from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from db.models.documento import Documento
from schemes.documentoScheme import DocumentoCreateScheme, DocumentoResponse
from db.database import get_db
from servicios.compartido.verificarEstadoActivo import verificarEstadoActivo
from servicios.permisos.permisoMiddleware import verificarPermisoUsuario
from utils.error.errors import ErrorResponse, ServiceException
from utils.hash.hashTabla import generarHash
from utils.responses import generate_response
import logging
from servicios.compartido.documento.obtenerDocumento import obtenerDocumentoPorId, obtenerDocumentos
from servicios.cdd.cdd import obtenerDocumentoPorCddId, obtenerDocumentosCdd

logger = logging.getLogger("Expediente")

router = APIRouter()


# GET: Obtener documento por ID
@router.get("/documento/{documentoId}",
            description="Consulta el documento",
            response_model=List[DocumentoResponse])
async def getDocumento(request: Request, documentoId: int, usuarioId: int = 1, db: Session = Depends(get_db)):
    """
    Endpoint para consultar el contenido de un documento. Este se encarga de la validación de 
    la existencia del documento y que los permisos se cumplan.

    Parámetros:
        - documentoId: ID del documento a consultar en la base de datos.

    Retorno:
        - RedirectResponse a la URL del CDD.

    """
    try:
        # ---- PERMISOS
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Consultar Expediente"], db)


        # ---- DOCUMENTO

        # Obtener el documento
        documentoResult = await obtenerDocumentoPorId(documentoId, db)

        # Verificar si el documento se encuentra activo
        documentoActivo = verificarEstadoActivo([documentoResult])


        logger.debug(f"Documento obtenido: {documentoActivo}")
        # Devolver el documento
        return documentoActivo

    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e


# GET: Obtener contenido del documento por ID
@router.get("/documento/{documentoId}/contenido",
            description="Consulta el documento y redirecciona a la URL de CDD")
async def getDocumento(request: Request, documentoId: int, usuarioId: int = 1, db: Session = Depends(get_db)):
    """
    Endpoint para consultar el contenido de un documento. Este se encarga de la validación de 
    la existencia del documento y que los permisos se cumplan.

    Parámetros:
        - documentoId: ID del documento a consultar en la base de datos.

    Retorno:
        - RedirectResponse a la URL del CDD.

    """
    try:
        # ---- PERMISOS
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Consultar Expediente"], db)
        

        # ---- DOCUMENTO

        # Obtener el documento
        documentoResult = await obtenerDocumentoPorId(documentoId, db)


        # ---- CDD
        documentoResultCDD = await obtenerDocumentoPorCddId(documentoResult.cddId)


        # ---- REDIRECCIONAMIENTO
        # Redireccionar a la URL del CDD
        #link = f"https://factorialhr.com.ar/blog/renuncia-laboral/"
        urlDocCdd = documentoResultCDD["data"]["url"]

        logger.debug(f"Documento obtenido por id: {documentoResult}")
        return RedirectResponse(url=urlDocCdd)

    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e


# GET: Obtener todos los documentos
@router.get("/documento", 
            response_model=List[DocumentoResponse], 
            tags=["Documento"],
            summary="Obtener una lista de documentos", 
            description="Obtiene una lista paginada de documentos",
            status_code=200)
async def getDocumentos(request:Request,db: Session = Depends(get_db)):
    """
    Obtener todos los documentos disponibles.
    """
    try:
        usuarioAplicacionId = request.headers.get("X-Usuario-Id")

        # Verificar permisos
        await verificarPermisoUsuario(usuarioAplicacionId, ["Consultar Expediente"], db)
        
        # Obtener todos los documentos
        documentos = await obtenerDocumentos(db)

        #Filtrar documentos por activo
        documentosActivos = verificarEstadoActivo(documentos)


        logger.debug(f"Lista de documentos: {documentosActivos}")
        return documentosActivos
    
    except SQLAlchemyError as e:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except Exception as exc:
        raise ServiceException(status_code=500, detail="Error al obtener la lista de documentos", extra={"error": str(exc)})
