from db.databaseUtils import realizarConexionBD
from schemes.documentoScheme import DocumentoResponse
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from db.models.documento import Documento

# Función que obtiene un documento por su id
async def obtenerDocumentoPorId(documentoId: int, db) -> DocumentoResponse:
    """
    Parámetros:
        - documentoId: int

    Retorna:
        - DocumentoResponse

    Excepciones:
        - ServiceException(404, "El documento solicitado no existe", extra={"documento_id": documentoId})
        - ServiceException(404, "El documento solicitado se encuentra inactivo", extra={"documento_id": documentoId})
        - ServiceException(500, "Error al obtener el documento", extra={"error": str(e), "documento_id": documentoId})
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_documento_id": documentoId
        }
        # Obtener el documento
        documentoResultList = await realizarConexionBD(procNombre="obtenerDocumentoPorId", 
                                                       procParams=params, 
                                                       db=db, 
                                                       model=DocumentoResponse)

        documentoResult = documentoResultList["rows"]

        if not documentoResult:
            raise ServiceException(status_code=404, detail="El documento solicitado no existe", extra={"documento_id": documentoId})

        documentoResult = documentoResult[0]

        # Verificación del hash
        if not verificarHash(documentoResult, Documento, documentoResult.hashTabla):
            raise ServiceException(status_code=500, detail="El hash del documento no coincide", extra={"documento_id": documentoId})

        return documentoResult
    
    except ServiceException as e:
        raise e

    except Exception as e:
        if f"El documento con id {documentoId} no existe" in str(e):
            raise ServiceException(status_code=404, detail="El documento solicitado no existe", extra={"documento_id": documentoId})
        elif f"El documento con id {documentoId} no se encuentra activo" in str(e):
            raise ServiceException(status_code=404, detail="El documento solicitado se encuentra inactivo", extra={"documento_id": documentoId})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el documento", extra={"error": str(e), "documento_id": documentoId})
        

# Función que obtiene todos los documentos relacionados a un expediente
async def obtenerDocumentosPorExpedienteId(expedienteId, db) -> list[DocumentoResponse]:
    """
    Parámetros:
        - expedienteId: int

    Retorna:
        - list[DocumentoResponse]

    Excepciones:
        - 
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_expedienteId": expedienteId
        }
        # Obtener los documentos
        documentosResultList = await realizarConexionBD(procNombre="obtenerDocumentosPorExpedienteId", procParams=params, db=db, model=DocumentoResponse)

        documentosList = documentosResultList["rows"]

        # Verificación del hash
        for documento in documentosList:
            if not verificarHash(documento, Documento, documento.hashTabla):
                raise ServiceException(status_code=500, detail="El hash del documento no coincide", extra={"nombreArchivo": documento.nombreArchivo})

        return documentosList
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El expediente con id {expedienteId} no existe" in str(e):
            raise ServiceException(status_code=404, detail="No se encuentra el expediente solicitado", extra={"expedienteId": expedienteId})
        elif f"El expediente con id {expedienteId} no se encuentra activo" in str(e):
            raise ServiceException(status_code=404, detail="El expediente solicitado se encuentra inactivo", extra={"expedienteId": expedienteId})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el expediente", extra={"error": str(e), "expedienteId": expedienteId})

async def obtenerDocumentos(db) -> list[DocumentoResponse]:
    """
    Parámetros:
        - 

    Retorna:
        - list[DocumentoResponse]

    Excepciones:
        - 
    """
    try:
        # Obtener los documentos
        documentosResultList = await realizarConexionBD(procNombre="obtenerDocumentos",procParams=None ,db=db, model=DocumentoResponse)

        documentosList = documentosResultList["rows"]

        # Verificación del hash
        for documento in documentosList:
            if not verificarHash(documento, Documento, documento.hashTabla):
                raise ServiceException(status_code=500, detail="El hash del documento no coincide", extra={"nombreArchivo": documento.nombreArchivo})

        return documentosList
    
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al obtener los documentos", extra={"error": str(e)})