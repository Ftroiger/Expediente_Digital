from db.models.expediente import Expediente
from utils.error.errors import ServiceException
from db.databaseUtils import realizarConexionBD
from sqlalchemy.orm import Session

from utils.paramBuilders import buildExpedienteParams

async def insertarExpedienteBdd(tipoExpedienteId: int, expedientePadreId: int, numeroExpediente: str, areaIniciadoraId: int,usuarioFisicoId: int, usuarioCreadorId: int, asuntoExpediente: str, visibilidadExpediente: str, temaNombre: str, foliosApertura: int, idExpedienteSirad: int, db: Session) -> Expediente:
    """
    Inserts a new expediente record into the database.

    This asynchronous function constructs the parameters for a new expediente
    using the provided details and inserts it into the database by calling
    a stored procedure. If an expediente with the same number already exists,
    a ServiceException is raised.

    Parameters:
    - tipoExpedienteId (int): The ID of the expediente type.
    - expedientePadreId (int): The ID of the parent expediente.
    - numeroExpediente (str): The expediente number.
    - areaIniciadoraId (int): The ID of the initiating area.
    - usuarioCreadorId (int): The ID of the creating user.
    - asuntoExpediente (str): The subject of the expediente.
    - visibilidadExpediente (str): The visibility status of the expediente.
    - temaNombre (str): The name of the theme.
    - foliosApertura (int): The number of opening folios.
    - idExpedienteSirad (int): The ID of the expediente in SIRAD.
    - db (Session): The database session.

    Returns:
    - dict: The result of the expediente insertion.

    """
    try:
        params = buildExpedienteParams(
            tipoExpedienteId,
            expedientePadreId,
            numeroExpediente,
            areaIniciadoraId,
            usuarioFisicoId,
            usuarioCreadorId,
            asuntoExpediente,
            visibilidadExpediente,
            temaNombre,
            foliosApertura,
            idExpedienteSirad
        )
        expedienteResultDict = await realizarConexionBD("crearExpediente", params, db, keep=True, model=Expediente)
        
        expedienteResult = expedienteResultDict["rows"][0]

        return expedienteResult
    
    except ServiceException as e:
        raise e

    except Exception as e:
        if f"Ya existe expediente con este numero de expediente" in str(e):
            raise ServiceException(404, "Ya existe expediente con este numero de expediente", extra={"numeroExpediente": numeroExpediente})
        else:
            raise ServiceException(500, "Error al insertar expediente en CDD", extra={"error": str(e), "numeroExpediente": numeroExpediente})