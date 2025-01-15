from db.databaseUtils import realizarConexionBD
from schemes.rolScheme import rolCreate, rolResponse
from utils.error.errors import ServiceException
from db.models.rol import Rol
from utils.paramBuilders import buildRolParams

async def crearRol(rol: rolCreate, db) -> rolResponse:
    """
    parámetros:
        - rol: rolCreate
        - db: Session

    retorna:
        - rolResponse

    Exepciones:
        - ServiceException(400, "El rol ya existe")
        - ServiceException(500, "Error al crear el rol", extra={"error": str(e)})
    """
    try:
        # Crear parámetros y ejecutar la consulta
        params = buildRolParams(rol.nombreRol, rol.descripcionRol)
        rolResultDict = await realizarConexionBD("crearRol", params, db, keep=True, model=Rol)

        rolResult = rolResultDict["rows"][0]

        # Mapea el resultado al esquema de respuesta
        return rolResponse(
            rolId=rolResult.rolId,
            nombreRol=rolResult.nombreRol,
            descripcionRol=rolResult.descripcionRol,
            activo=rolResult.activo,
            hashTabla=rolResult.hashTabla,
        )
    
    except ServiceException as e:
        raise e

    except Exception as e:
        if f"El rol ya existe" in str(e):
            raise ServiceException(status_code=400, detail="El rol ya se encuentra registrado", extra={"nombreRol": rol.nombreRol})
        else:
            raise ServiceException(status_code=500, detail="Error al crear el rol", extra={"error": str(e)})