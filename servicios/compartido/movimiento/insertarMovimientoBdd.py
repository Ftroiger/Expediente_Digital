from db.models.movimiento import Movimiento
from utils.error.errors import ServiceException
from db.databaseUtils import realizarConexionBD
from sqlalchemy.orm import Session

from utils.paramBuilders import buildMovimientoParams

async def insertarMovimientoBdd(tramiteId, expedienteResultId, usuarioId, usuarioOrigenId, areaOrigenId,areaDestinoId, observaciones, db: Session) -> Movimiento:
    """
    Inserts a movement record into the database.

    This asynchronous function constructs parameters for a movement record
    and executes a stored procedure to insert the record into the database.
    If the insertion is successful, it returns the first result from the
    operation. If an error occurs, it raises a ServiceException with
    appropriate details.

    Parameters:
    - tramiteId: Identifier for the tramite.
    - expedienteResultId: Identifier for the expediente result.
    - usuarioId: Identifier for the application user.
    - usuarioOrigenId: Identifier for the creator user.
    - areaDestinoId: Identifier for the destination area.
    - observaciones: Observations related to the movement.
    - db: Database session for executing the operation.

    Returns:
    - The first result from the movement insertion operation.

    Raises:
    - ServiceException: If the expediente does not exist or if there is
    an error during the insertion process.
    """
    try:
        params = buildMovimientoParams(
            tramiteId, 
            expedienteResultId, 
            usuarioId, 
            usuarioOrigenId, 
            areaOrigenId,
            areaDestinoId, 
            observaciones
        )

        movimientoResultDict = await realizarConexionBD("crearMovimiento", params, db, keep=True, model=Movimiento)

        movimientoResult = movimientoResultDict["rows"][0]
        
        return movimientoResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"El expediente no existe" in str(e):
            raise ServiceException(404, "El expediente no existe", extra={"expedienteResultId": expedienteResultId})
        else:
            raise ServiceException(500, "Error al insertar movimiento en CDD", extra={"error": str(e), "expedienteResultId": expedienteResultId})