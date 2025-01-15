from utils.error.errors import ServiceException
from utils.paramBuilders import buildRelacionParams
from db.databaseUtils import realizarConexionBD

async def crearRelacionDocumentoMovimiento(movimientoId, documentoId, folioInicial, folioFinal, db):
    """
    Crea una relación entre un documento y un movimiento en la base de datos.

    Parámetros:
        movimientoId: int -> ID del movimiento.
        documentoId: int -> ID del documento.
        folioInicial: int / None -> Folio inicial del documento en relación con el movimiento.
        folioFinal: int / None -> Folio final del documento en relación con el movimiento.
        db: Session -> Conexión activa a la base de datos.

    Retorna:
        dict -> Resultado de la relación creada o un ErrorResponse en caso de error.
    """
    try:
        # Construir los parámetros de la relación
        relacionParams = buildRelacionParams(movimientoId, documentoId, folioInicial, folioFinal)
        
        # Insertar la relación en la base de datos
        relacionResultDict = await realizarConexionBD("crearRelacion", relacionParams, db, keep=True)

        # Extraer la lista de resultados
        relacionResult = relacionResultDict["rows"][0]
        
        # Retornar el primer elemento de la lista de resultados
        return relacionResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if "Ya existe una relación con este id de movimiento" in str(e):
            raise ServiceException(404, "Ya existe una relación con este id de movimiento e id de documento", extra={"movimientoId": movimientoId, "documentoId": documentoId})
        else:
            raise ServiceException(500, "Error al crear la relación entre el documento y el movimiento", extra={"error": str(e), "movimientoId": movimientoId, "documentoId": documentoId})