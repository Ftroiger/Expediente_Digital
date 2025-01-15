from db.databaseUtils import realizarConexionBD
from schemes.permisoScheme import PermisoCreate
from servicios.compartido.rol.obtenerRoles import obtenerRolPorNombre
from utils.error.errors import ServiceException
from db.models.permiso import Permiso
from utils.paramBuilders import buildPermisoParams
from schemes.permisoScheme import PermisoResponse

async def crearPermiso(permiso: PermisoCreate, db) -> PermisoResponse:
    """
    parámetros:
        - permiso: permisoCreate
        - db: Session

    retorna:
        - permisoResponse

    Excepciones:
        - ServiceException(400, "El permiso ya existe")
        - ServiceException(500, "Error al crear el permiso", extra={"error": str(e)})
    """
    try:
        # Paso 1: Obtener el rol por nombre
        rolResult = await obtenerRolPorNombre(permiso.nombreRol, db)

        # Paso 2: Crear el permiso (sin el nombre del rol)
        params = buildPermisoParams(
            permiso.nombrePermiso,
            permiso.descripcionPermiso
        )
        permisoResultDict = await realizarConexionBD("crearPermiso", params, db, keep=True, model=Permiso)
        permisoResult = permisoResultDict["rows"][0]

        # Paso 3: Crear la relación en la tabla intermedia
    
        relacionParams = {
            "p_rol_id": rolResult.rolId,  # Cambiado: usar atributo, no clave de diccionario
            "p_permiso_id": permisoResult.permisoId # Cambiado: usar atributo, no clave de diccionario
        }

        relacionResultDict = await realizarConexionBD("crearRelacionRolPermiso", relacionParams, db, keep=True)
        relacionResult = relacionResultDict["rows"][0]

        # Retornar el permiso creado (puedes incluir detalles de la relación si es necesario)
        return {
            **permisoResult.__dict__,  # Convertimos el objeto a diccionario
            "rolXPermiso": relacionResult  # Incluye los detalles de la relación si lo necesitas
        }

    except ServiceException as e:
        raise e
    except Exception as e:
        if f"La relación entre el rol y el permiso ya existe" in str(e):
            raise ServiceException(status_code=400, detail="La relación entre el rol y el permiso ya existe")
        elif f"Ya existe un permiso con el nombre ingresado" in str(e):
            raise ServiceException(status_code=400, detail="El permiso con el nombre ingresado ya existe", extra={"permiso": permiso.nombrePermiso})
        elif f"El permiso no existe" in str(e):
            raise ServiceException(status_code=400, detail="El permiso no se encuentra", extra={"permiso": permiso.nombrePermiso})
        elif f"El rol no existe" in str(e):
            raise ServiceException(status_code=400, detail="El rol no se encuentra", extra={"rol": permiso.nombreRol})
        else:
            raise ServiceException(status_code=500, detail="Error al crear el permiso", extra={"error": str(e)})
