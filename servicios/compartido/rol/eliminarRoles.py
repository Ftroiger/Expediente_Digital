from db.databaseUtils import realizarConexionBD
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from db.models.rol import Rol

async def eliminarRolPorNombre(nombreRol: str, db) -> Rol:
    """
    parametros:
        - nombreRol: str
        - db: Session

    retorna:
        - Boolean

    Exepciones:
        - ServiceException(400, "El rol no existe")
        - ServiceException(500, "Error al eliminar el rol", extra={"error": str(e)})
    """
    try:
        params = {"p_nombre_rol": nombreRol}
        rolResult = await realizarConexionBD("eliminarRolPorNombre", params, db, keep=True)

        rol = rolResult["rows"][0]

        # Obtener los permisos asociados al rol
        params = {
            "p_nombre_rol": nombreRol
        }
        rolXPermisoResult = await realizarConexionBD("obtenerPermisosPorNombreRol", params, db, keep=True)

        rolesXPermisos = rolXPermisoResult["rows"]

        # Si tiene permisos asociados, se eliminan las relaciones
        if len(rolesXPermisos) > 0:
            params = {"p_rol_id": rol["rolId"]}
            rolXPermisoResult = await realizarConexionBD("eliminarRolXPermisoPorRolId", params, db, keep=True)
            rolesXPermisos = rolXPermisoResult["rows"]
        
        return {
            "eliminarRolPorNombre": True,
            "rol": rol, 
            "rolXPermiso": rolesXPermisos
        }
        
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"No existe un rol con el nombre" in str(e):
            raise ServiceException(status_code=400, detail="El rol no se encuentra registrado", extra={"nombreRol": nombreRol})
        elif f"ya que tiene usuarios asociados" in str(e):
            raise ServiceException(status_code=400, detail="El rol no se puede eliminar ya que tiene usuarios asociados", extra={"nombreRol": nombreRol})
        else:
            raise ServiceException(status_code=500, detail="Error al eliminar el rol", extra={"error": str(e)})