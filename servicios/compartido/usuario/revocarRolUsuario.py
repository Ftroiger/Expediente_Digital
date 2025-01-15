from sqlalchemy.orm import Session
from db.databaseUtils import realizarConexionBD
from db.models.rolXUsuario import RolXUsuario
from utils.error.errors import ServiceException

# Funcion que se encarga de revocar un rol a un usuario
async def revocarRolUsuario(usuarioId: int, db: Session):
    try:
        

        # Eliminar Relacion rolXUsuario
        params = {
            "p_usuario_id": usuarioId
        }
        rolXUsuarioEliminadoResult = await realizarConexionBD(
                            procNombre="eliminarRolXUsuarioPorUsuarioId", 
                            procParams=params, 
                            db=db, 
                            model=RolXUsuario)
        
        params = {
            "p_usuario_id": usuarioId,
            "p_nombre_rol": "Usuario Fisico"
        }

        # Asignamos al usuario rol usuario Fisico
        rolXUsuarioCreadoResult = await realizarConexionBD(
                            procNombre="asignarRolAUsuario", 
                            procParams=params, 
                            db=db, 
                            model=RolXUsuario)
        rolesXUsuariosEliminados = rolXUsuarioEliminadoResult["rows"]
        rolXUsuarioCreado = rolXUsuarioCreadoResult["rows"][0]
        return {
            "eliminarRolDeUsuario": True,
            "rolesXUsuariosEliminados": rolesXUsuariosEliminados, 
            "rolXUsuarioCreado": rolXUsuarioCreado
        }
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(status_code=500, 
                               detail="Error al revocar rol de usuario", 
                               extra={"error": str(e), 
                                      "usuarioId": usuarioId})
