from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.databaseUtils import realizarConexionBD
from db.models.notificacion import Notificacion
from db.models.usuario import Usuario
from servicios.compartido.verificarEstadoActivo import verificarEstadoActivo
from servicios.compartido.usuario.obtenerUsuario import verificarExistenciaUsuario, verificarExistenciaUsuarioAplicacion
from utils.error.errors import ServiceException
from servicios.hash.verificarHash import verificarHash

# Funcion que da de baja logica a usuario de la base de datos
async def darBajaUsuario(usuarioAplicacionId: int, db: Session):
    try:
        params = {
            "p_usuario_id": usuarioAplicacionId
        }
        # Verificar la existencia del usuario
        existeUsuario = await verificarExistenciaUsuario(usuarioAplicacionId, db)

        if not existeUsuario:
            raise ServiceException(status_code=404, detail="No se encuentra el usuario solicitado", extra={"usuarioAplicacionId": usuarioAplicacionId})

        # Dar de baja el usuario
        bajaUsuarioResult = await realizarConexionBD(procNombre="darBajaUsuarioAplicacion", procParams=params, db=db, model=Usuario)

        bajaUsuarioLista = bajaUsuarioResult["rows"]

        # Verificar estado activo
        verificarEstadoActivo(bajaUsuarioLista)

        bajaUsuario = bajaUsuarioLista[0]

        # Verificar hash
        if not verificarHash(bajaUsuario, Usuario, bajaUsuario.hashTabla):
            raise ServiceException(status_code=500, detail="El hash del usuario no coincide", extra={"usuario_id": bajaUsuario.usuarioId})


        return bajaUsuario
    
    except ServiceException as e:
        raise e

    except Exception as e:
        if "No existe un usuario con AplcacionID " in str(e):
            raise ServiceException(status_code=404, detail="No se encuentra el usuario solicitado", extra={"usuarioAplicacionId": usuarioAplicacionId})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el usuario", extra={"error": str(e), "usuarioAplicacionId": usuarioAplicacionId})
        


# Función de pedido de baja de usuario aplicación
async def pedidoDarBajaUsuarioAplicacion(usuarioId: int, usuarioAplicacionId: int, descripcionNotificacion: str, db: Session = Depends(get_db)):
    try:
        # Verificar la existencia del usuario
        existeUsuario = await verificarExistenciaUsuario(usuarioAplicacionId, db)

        if not existeUsuario:
            raise ServiceException(status_code=404, detail="No se encuentra el usuario solicitado", extra={"usuarioAplicacionId": usuarioAplicacionId})

        # Verificar que el usuarioAplicacionId no se encuentre en la lista de usuarios a los que se les ha pedido baja
        params = {
            "p_usuario_afectado_id": usuarioAplicacionId
        }

        existeUsuarioAplicacion = await realizarConexionBD(procNombre="verificarSolicitudBaja", 
                                                           procParams=params, 
                                                           db=db)
        

        if existeUsuarioAplicacion["rows"][0]["verificarsolicitudbaja"]:
            raise ServiceException(status_code=400, detail="Ya se ha solicitado la baja de este usuario", extra={"usuarioAplicacionId": usuarioAplicacionId})

        # Armar parámetros para pedido de baja notificacion
        params = {
            "p_usuario_id": usuarioId,
            "p_usuario_afectado_id": usuarioAplicacionId,
            "p_descripcion_notificacion": descripcionNotificacion
        }

        # Realizar conexión a la base de datos
        notificacionResult = await realizarConexionBD(procNombre="crearNotificacionBaja", procParams=params, db=db, model=Notificacion)

        notificacion = notificacionResult["rows"][0]

        return notificacion

    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al pedido de baja de usuario", extra={"error": str(e), "usuarioAplicacionId": usuarioAplicacionId})
