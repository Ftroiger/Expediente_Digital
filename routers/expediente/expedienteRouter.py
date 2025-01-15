import base64
from io import BytesIO
import logging
import json
from fastapi import APIRouter, Depends, Form, Request, UploadFile, File
from pydantic_core import ValidationError
from fastapi.exceptions import HTTPException
import qrcode
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from db.models.expediente import Expediente
from schemes.expedienteScheme import ActualizarExpediente, ExpedienteCreateScheme, ExpedienteResponse
from schemes.siradScheme import TemaScheme
from db.database import get_db
from servicios.compartido.verificarEstadoActivo import verificarEstadoActivo
from servicios.compartido.auditoria.completarAuditoria import completarAuditoriaExpediente, completarAuditoriaMovimiento, completarAuditoriaDocumento, completarAuditoriaDocumentoXMovimiento
from servicios.compartido.documento.obtenerDocumento import obtenerDocumentosPorExpedienteId 
from servicios.compartido.expediente.obtenerExpediente import obtenerExpedientePorNumeroExpediente, obtenerExpedientes
from servicios.compartido.expediente.insertarExpedienteBdd import insertarExpedienteBdd
from servicios.compartido.movimiento.insertarMovimientoBdd import insertarMovimientoBdd
from servicios.compartido.expediente.obtenerExpedienteTipo import obtenerExpedienteTipoExpediente
from servicios.compartido.usuario.obtenerUsuario import obtenerUsuarioPorId
from schemes.expedienteScheme import ActualizarExpediente, ExpedienteCreateScheme, ExpedienteResponse, OrganigramaEntry
from schemes.siradScheme import TemaScheme
from schemes.documentoScheme import DocumentoResponse, DocumentoQRCodeResponse
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ErrorResponse, ServiceException
from utils.hash.hashTabla import generarHash
from servicios.permisos.permisoMiddleware import verificarPermisoUsuario
from servicios.simulaciones.simulacion import generarCaratula
from utils.documentoTools import contarPaginasDocumento, contieneFirmaDigitalPDF
from servicios.compartido.documento.procesarDocumentosYRelacionar import procesarDocumentoYRelacionar
from servicios.sirad.sirad import crearDocumentoSirad, consultarTemas, generarCaratulaSirad
from servicios.compartido.expediente.verificarExistenciaExpediente import verificarExistenciaExpedientePorNumero
from db.models.documento import Documento
from servicios.baseUnica.apiBaseUnica import loginBaseUnica, getOrganigrama, getDependenciaById

from servicios.compartido.obtenerDatosAuditoria import obtenerAuditoriaHeader


# Funciones intermedias
from servicios.compartido.foliaje import procesarFoliajeDocumentos
from utils.responses import generate_response

# Configurar el logging
logger = logging.getLogger("Expediente")

router = APIRouter()

@router.get("/expediente/temas", response_model=List[TemaScheme])
async def obtener_temas():
    """
    Endpoint para obtener la lista de temas desde SIRAD.
    """
    try:
        temas = await consultarTemas()

        logger.debug("Temas obtenidos correctamente")
        return temas

    except ServiceException as e:
        raise e
    except Exception as e:
        raise e


@router.get("/expediente/organigrama",
            summary="Obtener organigrama de la municipalidad",
            response_model=List[OrganigramaEntry],
            description="Obtiene una lista de las dependencias (áreas) del organigrama municipal")
async def organigramaEndpoint():
    """
    Endpoint para obtener las dependencias del organigrama municipal.
    """
    try:
        organigrama = await getOrganigrama()
        logger.debug("Organigrama obtenido correctamente")
        return organigrama
    except ServiceException as e:
        raise e
    except Exception as e:
        raise e


@router.get("/expediente/dependencia/{idDependencia}",
            summary="Obtener dependencia por ID",
            description="Obtiene la información de una dependencia (área) por su ID",
            response_model=List[OrganigramaEntry])
async def dependenciaByIdEndpoint(idDependencia: int):
    """
    Endpoint para obtener una dependencia (área) por su ID.
    """
    try:
        dependencia = await getDependenciaById(idDependencia)
        logger.debug("Dependencia obtenida correctamente")
        return dependencia
    except ServiceException as e:
        raise e
    except Exception as e:
        raise e
    

# Ruta para obtener lista de expedientes
@router.get("/expediente", 
            response_model=List[ExpedienteResponse], 
            summary="Obtener una lista de expedientes", 
            description="Obtiene una lista paginada de expedientes")
async def getExpedientes(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Validación de los parámetros 'skip' y 'limit'
    if skip < 0 or limit < 1:
        raise ServiceException(status_code=400, detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a cero", extra={"skip": skip, "limit": limit})
    
    try:
        # ---- PERMISOS
        # Extraer usuarioId de los headers
        usuarioId = request.headers.get("X-Usuario-Id")
        # Verifica el permiso del usuario pasando el request para los headers
        await verificarPermisoUsuario(usuarioId, ["Consultar Expediente"], db)

        # Consulta a la base de datos con paginación
        expedientes = await obtenerExpedientes(db, skip, limit)

        # Filtrar expedientes activos
        expedientesFront=verificarEstadoActivo(expedientes)

        
        # Verificación de si se encontraron expedientes
        if not expedientes:
            raise ServiceException(status_code=404, detail="No se encontraron expedientes")
        
        logger.debug(f"Se obtuvieron los expediente {expedientesFront}")
        return expedientesFront
    
    except SQLAlchemyError as e:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ValidationError as e:
        db.rollback()
        raise e
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc
    

# Ruta para crear un nuevo expediente
@router.post("/expediente", 
             response_model=ExpedienteResponse, 
             summary="Crear nuevo expediente", 
             description="Crea un nuevo expediente en la base de datos")
async def crearExpediente(
                        request: Request,
                        jsonData: str = Form(...), # JSON data como un string
                        files: List[UploadFile] = File(...), # Lista de archivos subidos
                        db: Session = Depends(get_db)):
    """
    Endpoint para la creación de un nuevo expediente. El proceso implica la inserción en varias tablas, la validación
    de permisos y la integración con APIs externas para almacenar documentos y obtener información adicional del expediente.

    Parámetros:
        Expediente:
            - expedientePadreId: int / None
            - asuntoExpediente: str
            - visibilidadExpediente: str
            - areaIniciadorId: int
            - usuarioCreadorAplicacionId: int
            - temaNombre: str
        Movimiento:
            - tramiteId: int
            - usuarioAplicacionId: int
            - usuarioOrigenId: int
            - observaciones: str
            # - areaDestinoId: int
        SIRAD:
            - IdTema: int
            - IniciadorPersonaFisica: dict = {
                    Sexo: str,
                    Nombre: str,
                    Apellido: str,
                    NroDocumento: str,
                }
            - IniciadorPersonaJuridica: dict = {
                    Cuit: str,
                    RazonSocial: str,
                    Sucursal: dict = {
                        NomenclaturaCatastral: str,
                        Representante: dict = {
                            Sexo: str,
                            Nombre: str,
                            Apellido: str,
                            NroDocumento: str,
                        }
                    }
                }
            # - documentos: list[DocumentoCreateScheme] = [
                    {
                        firmaDigitalId: int / None
                        cddId: int / None
                        nombreArchivo: str
                        tipoDocumento: str / None
                        cantPaginas: int / None
                        firmado: bool / None
                        estado: bool / None
                        documentoOrigenId: int / None
                        activo: bool / None
                        hashTabla: str / None
                        orden: int
                        data: bytes
                    }
                ]

    """
    try:
        datosAuditoria=obtenerAuditoriaHeader(request)


        # ---- PARSEAR JSON DATA
        # Convertir json data a diccionario
        jsonDataDict = json.loads(jsonData)

       # Validar JSON data
        expedienteData = ExpedienteCreateScheme.model_validate_json(jsonData)

        # Obtener las claves del esquema
        esquemaClaves = set(ExpedienteCreateScheme.model_fields.keys())

        # Obtener las claves del JSON de entrada
        jsonClaves = set(jsonDataDict.keys())

        # Verificar si hay claves adicionales
        clavesAdicionales = jsonClaves - esquemaClaves
        if clavesAdicionales:
            raise ServiceException(status_code=400, detail="Claves adicionales en el JSON", extra={"clavesAdicionales": list(clavesAdicionales)})


        if all(file.size == 0 for file in files) and all(file.filename == "" for file in files):
            db.rollback()
            raise ServiceException(status_code=400, detail="No se encontraron archivos")
        

        db.begin()
    
    
        # ---- PERMISO
        # Extraer el usuarioId de los headers
        usuarioAplicacionId = request.headers.get("X-Usuario-Id")
        usuarioFisicoId = request.headers.get("X-Usuario-Responsable-Id")

        # Verificar permiso de creación de expediente
        await verificarPermisoUsuario(usuarioAplicacionId, ["Crear Expediente"], db)
        

        # ---- FOLIAJE

        # Procesar los archivos subidos
        archivosInfo = await procesarFoliajeDocumentos(0, files)

        # Registrar folios apertura del expediente
        expedienteFoliosApertura = 0
        for file in archivosInfo:
            expedienteFoliosApertura += file["cantidadPaginas"]


        # ---- SIRAD

        # Validar los datos de SIRAD
        expedienteData.sirad.validate(expedienteData.sirad.model_dump())

        # Convertir los datos validados a un diccionario
        parametrosSirad = expedienteData.sirad.model_dump()

        # Llamada a la función de simulación para generar un número de expediente único
        respuestaSirad = await crearDocumentoSirad(parametrosSirad)

        # Obtener el número de expediente único generado por SIRAD
        numeroExpediente = respuestaSirad["Mascara"]


        # Verificar que no exista un expediente con el mismo número utilizando la función modularizada
        expedienteExiste = await verificarExistenciaExpedientePorNumero(numeroExpediente, db)
        
        if expedienteExiste:
            db.rollback()
            raise ServiceException(400, "El expediente ya existe en la base de datos", extra={"numero_expediente": numeroExpediente})


        # Obtener id del expediente guardado en SIRAD
        idExpedienteSirad = respuestaSirad["Id"]
        asuntoExpediente = expedienteData.sirad.Asunto #Lo usamos para generar caratula
        areaIniciadoraId = expedienteData.areaIniciadoraId #Lo usamos para generar caratula
        temaExpediente = expedienteData.temaNombre #Lo usamos para generar caratula

        # ---- EXPEDIENTE
        # Obtener el número de expediente único generado por SIRAD
        numeroExpediente = respuestaSirad["Mascara"]

        # Obtener id del expediente guardado en SIRAD
        idExpedienteSirad = respuestaSirad["Id"]
        
        # Obtener el tipo de expediente
        tipoExpediente = await obtenerExpedienteTipoExpediente(db)
        # Insertar expediente y agarrar el resultado
        expedienteResult = await insertarExpedienteBdd(tipoExpediente.tipoExpedienteId, expedienteData.expedientePadreId, numeroExpediente, expedienteData.areaIniciadoraId, usuarioFisicoId, usuarioAplicacionId, expedienteData.sirad.Asunto, expedienteData.visibilidadExpediente, expedienteData.temaNombre, expedienteFoliosApertura, idExpedienteSirad, db)

        fechaCreacion = expedienteResult.fechaCreacion #Lo usamos para generar caratula

       
        # ---- MOVIMIENTO
        # Insertar movimiento y agarrar el resultado
        movimientoResult = await insertarMovimientoBdd(expedienteData.tramiteId, expedienteResult.expedienteId, usuarioFisicoId, usuarioAplicacionId,expedienteData.areaIniciadoraId, expedienteData.areaIniciadoraId, expedienteData.sirad.Observaciones, db)

        # ---- DOCUMENTOS - CARÁTULA

        caratulaSirad = await generarCaratulaSirad(idExpedienteSirad)

        if caratulaSirad["Error"]:
            db.rollback()
            raise ServiceException(status_code=500, detail="Error al generar la carátula por parte de SIRAD", extra={"error": caratulaSirad["Error"]})

        # Generar la carátula del expediente
        caratula = await generarCaratula(numeroExpediente = numeroExpediente, asuntoExpediente = asuntoExpediente, temaExpediente = temaExpediente, areaIniciadoraId = areaIniciadoraId, fechaCreacion = fechaCreacion)

        # Verificar si hubo un error al generar la carátula
        if caratula["Error"]:
            db.rollback()
            raise ServiceException(status_code=500, detail="Error al generar la carátula", extra={"error": caratula["Error"]})

        # Contar las páginas de la carátula
        cantPaginasCaratula = contarPaginasDocumento(caratula["DocumentBytes"], "PDF")

        caratulaInfo = {
            "nombre": caratula["DocumentName"],
            "contenido": caratula["DocumentBytes"],
            "cantidadPaginas": cantPaginasCaratula,
            "firmado": False
        }

        # Procesar la carátula y relacionarla con el movimiento
        documentoXMovimientoResult =await procesarDocumentoYRelacionar(caratulaInfo, movimientoResult.movimientoId, db, cuilOperador="20-12345678-6", cuilPropietario="20-12345678-6")
        await completarAuditoriaDocumento(
            documentoId=documentoXMovimientoResult["documentoId"], 
            usuarioFisicoId=usuarioFisicoId,
            usuarioAplicacionId=usuarioAplicacionId,
            headerData=datosAuditoria,
            db=db
        )
        await completarAuditoriaDocumentoXMovimiento(
                documentoXMovimientoId=documentoXMovimientoResult["documentoXMovimientoId"],
                usuarioFisicoId=usuarioFisicoId,
                usuarioAplicacionId=usuarioAplicacionId,
                headerData=datosAuditoria,
                db=db
            )
        # ---- DOCUMENTOS Y RELACIONES CON MOVIMIENTO

        for documento in archivosInfo:
            documentoXMovimientoResult=await procesarDocumentoYRelacionar(documento, movimientoResult.movimientoId, db, cuilOperador="20-12345678-6", cuilPropietario="20-12345678-6")
            await completarAuditoriaDocumento(
                documentoId=documentoXMovimientoResult["documentoId"],
                usuarioFisicoId=usuarioFisicoId,
                usuarioAplicacionId = usuarioAplicacionId,
                headerData=datosAuditoria,
                db=db
            )
            await completarAuditoriaDocumentoXMovimiento(
                documentoXMovimientoId=documentoXMovimientoResult["documentoXMovimientoId"],
                usuarioFisicoId=usuarioFisicoId,
                usuarioAplicacionId=usuarioAplicacionId,
                headerData=datosAuditoria,
                db=db
            )

        # ---- AUDITORIA
        await completarAuditoriaExpediente(
            expedienteId=expedienteResult.expedienteId, 
            usuarioFisicoId=usuarioFisicoId,
            usuarioAplicacionId=usuarioAplicacionId,
            headerData=datosAuditoria,
            db=db
        )
        await completarAuditoriaMovimiento(
            movimientoId=movimientoResult.movimientoId, 
            usuarioFisicoId=usuarioFisicoId,
            usuarioAplicacionId=usuarioAplicacionId,
            headerData=datosAuditoria,
            db=db
        )
        # ---- COMMIT
        db.commit()
        
        logger.debug(f"Se creo expediente: {expedienteData}")
        return expedienteResult

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ValidationError as e:
        db.rollback()
        raise e
    except ServiceException as exc:
        db.rollback()
        raise exc
    except Exception as exc:
        db.rollback()
        raise exc


# Ruta para obtener todos los documentos dentro de un expediente
@router.get("/expediente/{expedienteNumero}/indiceDocumentos", 
            summary="Obtener documentos de un expediente",
            description="Obtiene una lista de documentos asociados a un expediente",
            response_model=List[DocumentoQRCodeResponse])
async def getIndiceDocumentosExpediente(request: Request, expedienteNumero: str, db: Session = Depends(get_db)):
    """
    Endpoint para obtener los campos nombreArchivo y cddId de los documentos asociados a un expediente específico
    para armar el indice del expediente.

    Parámetros:
        expedienteNumero: str -> Número único del expediente

    Respuesta:
        documentos
        {
            nombreArchivo = nombre asignado al archivo del documento 
            qr = codificacion de la ruta devuelta por el CddId
        }

    """
    try:
        # ---- PERMISOS
        # Extraer el usuarioId de los headers
        usuarioId = request.headers.get("X-Usuario-Id")
        # Verificar permiso de consulta de expediente
        await verificarPermisoUsuario(usuarioId, ["Consultar Expediente"], db)


        # Validar que el expediente exista y obtener el objeto expediente
        expedienteResult = await obtenerExpedientePorNumeroExpediente(expedienteNumero, db)

        # Obtener los documentos asociados al expediente
        documentosResultList = await obtenerDocumentosPorExpedienteId(expedienteResult.expedienteId, db)

        # URL documento by id
        UrlDocById = "http://localhost:8000/documento/"

        # return documentos
        documentos = []
        for doc in documentosResultList:

            # qr_data = str(doc.cddId)
            qr_data = UrlDocById + str(doc.documentoId)
            qr = qrcode.make(qr_data)
            buffered = BytesIO()
            qr.save(buffered, format="PNG")
            qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            documentos.append(DocumentoQRCodeResponse(
                nombreArchivo=doc.nombreArchivo,
                qr=qr_base64,
                usuarioCreador = expedienteResult.usuarioCreadorAplicacionId,
                documentoId = doc.documentoId,
                foliosInicial = doc.foliosInicial,
                folioFinal = doc.foliosFinal,
                areaOrigenId = doc.areaOrigenId,
                areaDestinoId = doc.areaDestinoId,
                cantPaginas = doc.cantPaginas,
                firmado = doc.firmado
            ))

        logger.debug(f"Se obtuvieron los documentos del expediente: {expedienteNumero}")
        return documentos
    
    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ValidationError as e:
        db.rollback()
        raise e
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc
   

@router.post("/expediente/loginBaseUnica",
            summary="Login en Base Única",
            description="Realiza un login en Base Única y devuelve el token de acceso")
async def loginBaseUnicaEndpoint():
    """
    Endpoint para realizar el login en Base Única y obtener el token de acceso.

    Respuesta
    {
        "token_type": "string",
        "access_token": "string",
        "expiration": "string"
    }
    """
    try:
        response = await loginBaseUnica()

        logger.debug("Login en Base Única exitoso")
        return {
            "token_type": response["token_type"],
            "access_token": response["access_token"],
            "expiration": response["expiration"]
        }
    except ServiceException as e:
        raise e
    except Exception as e:
        raise e