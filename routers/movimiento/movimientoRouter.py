import json
from fastapi import APIRouter, Depends, File, Request, UploadFile, Form
from fastapi.exceptions import HTTPException
from pydantic_core import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from db.models.movimiento import Movimiento
from db.models.expediente import Expediente
from servicios.baseUnica.apiBaseUnica import getDependenciaById
from servicios.compartido.auditoria.completarAuditoria import completarAuditoriaExpediente, completarAuditoriaMovimiento, completarAuditoriaDocumentoXMovimiento, completarAuditoriaDocumento
from servicios.compartido.expediente.actualizarExpedienteFolios import actualizarExpedienteFolios
from servicios.compartido.movimiento.obtenerMovimientos import obtenerMovimientos
from servicios.compartido.movimiento.insertarMovimientoBdd import insertarMovimientoBdd
from servicios.compartido.obtenerDatosAuditoria import obtenerAuditoriaHeader
from servicios.compartido.verificarEstadoActivo import verificarEstadoActivo
from servicios.permisos.permisoMiddleware import verificarPermiso, verificarPermisoUsuario
from schemes.movimientoScheme import MovimientoCreateScheme, MovimientoResponse, movimientoUpdate
from db.database import get_db
from db.databaseUtils import insertConnection, getConnection
from servicios.compartido.foliaje import procesarFoliajeDocumentos
from servicios.compartido.movimiento.obtenerMovimientos import obtenerMovimientosPorExpedienteId
from utils.paramBuilders import buildMovimientoParams
from utils.error.errors import ErrorResponse, ServiceException
from utils.hash.hashTabla import generarHash
from utils.responses import generate_response
from servicios.compartido.documento.procesarDocumentosYRelacionar import procesarDocumentoYRelacionar
import logging
from servicios.compartido.expediente.obtenerExpediente import obtenerExpedientePorNumeroExpediente

# Configuración del logger
logger = logging.getLogger("expediente")

router = APIRouter()

#POST: Crear un nuevo movimiento
@router.post("/expediente/{expedienteNumero}/movimiento", 
             response_model=list[MovimientoResponse],
             tags=["Movimiento"], 
             summary="Crear nuevo movimiento", 
             description="Crea un nuevo movimiento en la base de datos",)
async def crearMovimiento(
        request: Request,
        expedienteNumero: str,
        jsonData: str = Form(...), 
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db)):
    
    try:
        datosAuditoria=obtenerAuditoriaHeader(request)

        

        #---- VALIDACIONES

        #Validar expedienteNumero
        for val in expedienteNumero:
            if val == " ":
                raise ServiceException(status_code=400, detail="El numero de expediente no puede contener espacios", extra={"expedienteNumero": expedienteNumero})

        #Convertir json data a diccionario
        jsonDataDict = json.loads(jsonData)

       # Validar JSON data
        data = MovimientoCreateScheme.model_validate_json(jsonData)
        
        # Obtener las claves del esquema
        esquemaClaves = set(MovimientoCreateScheme.model_fields.keys())

        # Obtener las claves del JSON de entrada
        jsonClaves = set(jsonDataDict.keys())

        # Verificar si hay claves adicionales
        clavesAdicionales = jsonClaves - esquemaClaves
        if clavesAdicionales:
            raise ServiceException(status_code=400, detail="Claves adicionales en el JSON", extra={"clavesAdicionales": list(clavesAdicionales)})

        #Validar areaOrigenId existente
        await getDependenciaById(data.areaOrigenId)

        #Validar areaDestinoId existente
        for areaDestinoId in data.areasDestinoId:
            await getDependenciaById(areaDestinoId)

        db.begin()
        # Si no hay archivos, retornar un error
        if all(file.size == 0 for file in files) and all(file.filename == "" for file in files):
            db.rollback()
            raise ServiceException(status_code=400, detail="No se encontraron archivos", extra={"error": "Form-data 'files' con archivos adjuntos es requerido"})


        # ---- PERMISO
        # Extraer usuario id de los headers
        usuarioAplicacionId = request.headers.get("X-Usuario-Id")
        usuarioFisicoId = request.headers.get("X-Usuario-Responsable-Id")

        await verificarPermisoUsuario(usuarioAplicacionId, ["Mover Expediente"], db)
        
        # ---- EXPEDIENTE

        # Extraer el objeto expediente de la base de datos por el numeroExpediente
        expedienteResult = await obtenerExpedientePorNumeroExpediente(expedienteNumero, db)

        # ---- FOLIAJE

        # Procesar los archivos subidos
        archivosInfo = await procesarFoliajeDocumentos(expedienteResult.foliosActuales, files)
        
        # ---- ESTADO EXPEDIENTE 

        # Agregar verificacion del estadoExpediente segun su Id desde la tabla historialEstadoExpediente
        
        # ---- MOVIMIENTO
        movimientosReturn = []
        # Insertar movimiento y agarrar el resultado
        for areaDestinoId in data.areasDestinoId:
            movimientoResult = await insertarMovimientoBdd(data.tramiteId, expedienteResult.expedienteId, usuarioFisicoId, usuarioAplicacionId, data.areaOrigenId,areaDestinoId, data.observacionMovimiento, db)
            movimientosReturn.append(movimientoResult)
            await completarAuditoriaMovimiento(
                movimientoResult.movimientoId,
                usuarioFisicoId,
                usuarioAplicacionId,
                datosAuditoria,
                db
                )
        # ----- DOCUMENTOS Y RELACIONES CON MOVIMIENTO

            for documento in archivosInfo:
                documentoXMovimientoResult = await procesarDocumentoYRelacionar(
                    documento,
                    movimientoResult.movimientoId,
                    db,
                    cuilOperador="20-12345678-6",
                    cuilPropietario="20-12345678-6",
                )
                await completarAuditoriaDocumento(
                    documentoXMovimientoResult["documentoId"],
                    usuarioFisicoId,
                    usuarioAplicacionId,
                    datosAuditoria,
                    db
                )
                await completarAuditoriaDocumentoXMovimiento(
                    documentoXMovimientoResult["documentoXMovimientoId"],
                    usuarioFisicoId,
                    usuarioAplicacionId,
                    datosAuditoria,
                    db
                )

        # ---- ACTUALIZACIONES

        folios = expedienteResult.foliosActuales + sum([documento["cantidadPaginas"] for documento in archivosInfo])

        # Actualizar los folios del expediente
        expedienteFoliosResult = await actualizarExpedienteFolios(expedienteResult.expedienteId, folios, db)
        await completarAuditoriaExpediente(
            expedienteFoliosResult["expedienteId"],
            usuarioFisicoId,
            usuarioAplicacionId,
            datosAuditoria,
            db
        )
        # ----- COMMIT 
        db.commit()
        logger.debug(f"Se creo movimiento: {data}")
        return movimientosReturn
    
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
        raise exc
    

# GET: Obtener todos los movimientos de un expediente
@router.get("/expediente/{expedienteNumero}/movimiento",
            response_model=List[MovimientoResponse],
            tags=["Movimiento"],
            summary="Obtener movimientos de un expediente",
            description="Obtiene una lista de movimientos de un expediente específico",)
async def getMovimientosByExpediente(request: Request, expedienteNumero: str, db: Session = Depends(get_db)):
    try:
        # ---- PERMISO
        # Extraer usuario id de los headers
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Consultar Expediente"], db)

        # Extraer el objeto expediente de la base de datos por el numeroExpediente
        expedienteResult = await obtenerExpedientePorNumeroExpediente(expedienteNumero, db)

        # Filtrar los movimientos por el expedienteId
        movimientos = await obtenerMovimientosPorExpedienteId(expedienteResult.expedienteId, db)
       
        # Filtrar movimientos Activos
        movimientosFront = verificarEstadoActivo(movimientos)

        logger.debug(f"Se obtuvieron movimientos: {movimientosFront}")
        return movimientosFront
    
    except SQLAlchemyError as e:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ValidationError as e:
        db.rollback()
        raise ServiceException(status_code=400, detail="Error en la validación de los datos", extra={"error": str(e)})
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error al traer la lista de movimientos", extra={"error": str(exc)})

# GET: Obtener todos los movimientos
@router.get("/movimiento", 
            response_model=List[MovimientoResponse],
            tags=["Movimiento"],
            summary="Obtener una lista de movimientos", 
            description="Obtiene una lista paginada de movimiento",
            status_code=200,)
async def getMovimientos(request:Request ,db: Session = Depends(get_db)):
    try:
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Consultar Expediente"], db)

        movimientosResult = await obtenerMovimientos(db)
        
        # Filtrar los movimientos por activos
        movimientosResult = verificarEstadoActivo(movimientosResult)

        logger.debug(f"Se obtuvieron movimientos: {movimientosResult}")

        return movimientosResult
        
    
    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except Exception as exc:
        return ErrorResponse(status_code=500, detail="Error al traer la lista de movimientos")

# GET by ID: Obtener un movimiento por ID
@router.get("/movimiento/{idMovimiento}", 
            response_model=MovimientoResponse,
            tags=["Movimiento"], 
            summary="Obtener movimiento por ID",
            description="Obtiene un movimiento específico por su ID", 
            status_code=200,)
async def getMovimientoById(idMovimiento: int, db: Session = Depends(get_db)):
    try:
        movimiento = db.query(Movimiento).filter(Movimiento.movimientoId == idMovimiento).first()
        if not movimiento:
            return ErrorResponse(status_code=404, detail="Documento no encontrado")
        logger.debug(f"Se obtuvo movimiento por id: {movimiento}")
        return MovimientoResponse.model_validate(movimiento)
    
    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except Exception as exc:
        return ErrorResponse(status_code=500, detail="Error al traer el movimiento")
