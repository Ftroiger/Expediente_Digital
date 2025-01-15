from fastapi import Request
from sqlalchemy.orm import Session
from utils.error.errors import ErrorResponse, ServiceException
from sqlalchemy import text
from servicios.compartido.usuario.obtenerUsuario import verificarExistenciaUsuario

# Función para verificar los headers y el permiso de un sistema vertical
async def verificarPermisoUsuario(usuarioId: int, permiso: list[str], db: Session):
    """
    Función middleware que verifica los headers del request y si el usuario tiene permisos para realizar
    la acción solicitada.

    :param request: Request de FastAPI
    :param permiso: Acción que se desea realizar - Asume que la acción existe en la BD en el atributo 'nombre'
    :param db: Sesión de la base de datos para realizar los queries

    :return: None si el usuario tiene permisos, ErrorResponse si no tiene permisos
    """
    try:
        # Verificar la existencia de la aplicacion
        await verificarExistenciaUsuario(int(usuarioId), db)

        # Verificar cada permiso en la lista
        for p in permiso:
            await verificarPermiso(int(usuarioId), p, db)

    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, f"Error al verificar permisos", extra={"usuarioId": usuarioId, "permiso": permiso, "error": str(e)})

async def verificarPermiso(usuarioId: int, accion: str, db: Session):
    """
    Función middleware que verifica si el usuario tiene permisos para realizar
    la acción solicitada.

    :param usuarioAplicacion: ID de la aplicación
    :param accion: Acción que se desea realizar - Asume que la acción existe en la BD en la tabla 'Permiso' en el atributo 'nombre'
    :param db: Sesión de la base de datos para realizar los queries

    :return: None si el usuario tiene permisos, ErrorResponse si no tiene permisos

    """
    try:
        if db is None:
            raise ServiceException(500, f"Error al conectar a la base de datos", extra={"usuarioId": usuarioId, "accion": accion, "error": "Intento de verificación de permisos sin conexión a la base de datos"})
        # Llamar el procedimiento de verificar permiso
        query = (
            f"""SELECT * FROM public."verificarPermisoUsuario"(:p_usuario_id, :p_accion)"""
        )
        result = db.execute(text(query), {"p_usuario_id": int (usuarioId), "p_accion": accion})

        # Obtener el resultado de la consulta
        permiso = result.scalar()

        if not permiso:
            raise ServiceException(403, f"No tiene permisos para realizar esta acción", extra={"usuarioAplicacion": usuarioId, "accion": accion})

        return permiso
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"No existe un permiso con la acción" in str(e):
            raise ServiceException(403, f"No existe un permiso con la acción solicitada", extra={"usuarioAplicacion": usuarioId, "accion": accion})
        elif f"No tiene permisos para realizar esta acción" in str(e):
            raise ServiceException(403, f"No tiene permisos para realizar esta acción", extra={"usuarioAplicacion": usuarioId, "accion": accion})
        else:
            raise ServiceException(500, f"Error al verificar permisos", extra={"usuarioAplicacion": usuarioId, "accion": accion, "error": str(e)})

