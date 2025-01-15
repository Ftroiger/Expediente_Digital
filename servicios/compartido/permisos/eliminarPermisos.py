from db.databaseUtils import realizarConexionBD
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from db.models.permiso import Permiso

async def eliminarPermiso(nombrePermiso: str, db) -> Permiso:
    """
    parámetros:
        - nombrePermiso: str
        - db: Session

    retorna:
        - Boolean

    Exepciones:
        - ServiceException(400, "El permiso no existe")
        - ServiceException(500, "Error al eliminar el permiso", extra={"error": str(e)})
    """
    try:
        params = {"p_nombre_permiso": nombrePermiso}
        permisoResult = await realizarConexionBD("eliminarPermiso", params, db, keep=True)
        permiso = permisoResult["rows"][0]

        # Verificar si el permiso está vinculado a algún rol
        params = {"p_nombre_permiso": nombrePermiso}
        rolesResult = await realizarConexionBD("obtenerRolesPorNombrePermiso", params, db, keep=True)
        roles = rolesResult["rows"]

        # Si el permiso está vinculado a algún rol, se elimina la relación
        rolXPermiso = []
        if len(roles) > 0:
            params = {"p_permiso_id": permiso["permisoid"]}
            rolxPermisoResult = await realizarConexionBD("eliminarRolXPermisoPorPermisoId", params, db, keep=True)
            rolXPermiso = rolxPermisoResult["rows"]

        
        # Devolver el permiso y los rolXPermiso eliminados
        return {
            "permiso":permiso,
            "rolXPermiso":rolXPermiso
        }
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El permiso no existe" in str(e):
            raise ServiceException(status_code=400, detail="El permiso no se encuentra registrado", extra={"nombrePermiso": nombrePermiso})
        elif f"La relación entre el rol y el permiso no existe" in str(e):
            raise ServiceException(status_code=400, detail="La relación entre el rol y el permiso no existe", extra={"nombrePermiso": nombrePermiso})
        else:
            raise ServiceException(status_code=500, detail="Error al eliminar el permiso", extra={"error": str(e)})