from db.databaseUtils import realizarConexionBD
from utils.error.errors import ServiceException

# Función para verificar la existencia de un documento por su id
async def verificarExistenciaDocumentoPorId(documentoId: int, db) -> bool:
    """
    Verifica si existe un documento con el id proporcionado en la base de datos.

    Parámetros:
        - documentoId (int): El id del documento a verificar.
        - db: Conexión a la base de datos.

    Retorna:
        - True si el documento existe.
        - ServiceException si el documento no existe.
    """
    try:
        # Llamar a la función almacenada en la base de datos
        resultado = await realizarConexionBD(
            "obtenerDocumentoPorId",
            {"p_documento_id": documentoId},
            db,
            model=None,
            keep=True
        )

        documento = resultado.get("rows", [])[0]

        # Verificar si hay datos en 'rows'
        if not documento:
            raise ServiceException(
                status_code=404,
                detail="El documento solicitado no existe",
                extra={"documento_id": documentoId}
            )
        
        return True
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"El documento con id {documentoId} no existe" in str(e):
            raise ServiceException(
                status_code=404,
                detail="El documento solicitado no existe",
                extra={"documento_id": documentoId}
            )
        elif f"El documento con id {documentoId} no se encuentra activo" in str(e):
            raise ServiceException(
                status_code=404,
                detail="El documento solicitado se encuentra inactivo",
                extra={"documento_id": documentoId}
            )
        else:
            raise ServiceException(
                status_code=500,
                detail="Error al verificar la existencia del documento",
                extra={"error": str(e), "documento_id": documentoId}
            )