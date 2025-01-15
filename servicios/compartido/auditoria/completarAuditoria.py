
from db.databaseUtils import realizarConexionBD
from utils.error.errors import ServiceException


async def completarAuditoriaExpediente(
        expedienteId:int,
        usuarioFisicoId:int,
        usuarioAplicacionId:int,
        headerData:dict,
        db,
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:

        data = {
        "p_expediente_id": expedienteId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
        "p_usuario_aplicacion_responsable_id": usuarioAplicacionId,
    }
        auditoriaResulList = await realizarConexionBD("completarExpedienteAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"La usuarioId no pertenece a ningun Usuario" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El expediente Id no existe" in str(e):
            raise ServiceException(404, "Expediente no encontrado", extra={"expedienteId": expedienteId})
        elif f"El registro de auditoria con ese expediente Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"expedienteId": expedienteId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})
    
async def completarAuditoriaMovimiento(
        movimientoId:int,
        usuarioFisicoId:int,
        usuarioAplicacionId:int,
        headerData:dict,
        db,
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:

        data = {
        "p_movimiento_id": movimientoId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
        "p_usuario_aplicacion_responsable_id": usuarioAplicacionId,
    }
        auditoriaResulList = await realizarConexionBD("completarMovimientoAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"La usuarioId no pertenece a ningun Usuario" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El movimiento Id no existe" in str(e):
            raise ServiceException(404, "Movimiento no encontrado", extra={"movimientoId": movimientoId})
        elif f"El registro de auditoria con ese movimiento Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"movimientoId": movimientoId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})
    
async def completarAuditoriaDocumento(
        documentoId:int,
        usuarioFisicoId:int,
        usuarioAplicacionId:int,
        headerData:dict,
        db,
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:

        data = {
        "p_documento_id": documentoId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
        "p_usuario_aplicacion_responsable_id": usuarioAplicacionId,
    }
        auditoriaResulList = await realizarConexionBD("completarDocumentoAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"La usuarioId no pertenece a ningun Usuario" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El documento Id no existe" in str(e):
            raise ServiceException(404, "Documento no encontrado", extra={"documentoId": documentoId})
        elif f"El registro de auditoria con ese documento Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"documentoId": documentoId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})
    
async def completarAuditoriaDocumentoXMovimiento(
        documentoXMovimientoId:int,
        usuarioFisicoId:int,
        usuarioAplicacionId:int,
        headerData:dict,
        db,
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:

        data = {
        "p_documento_x_movimiento_id": documentoXMovimientoId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
        "p_usuario_aplicacion_responsable_id": usuarioAplicacionId,
    }
        auditoriaResulList = await realizarConexionBD("completarDocumentoXMovimientoAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"La usuarioId no pertenece a ningun Usuario" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId, "usuarioAplicacionId": usuarioAplicacionId})
        elif f"El documento x movimiento Id no existe" in str(e):
            raise ServiceException(404, "Documento x movimiento no encontrado", extra={"documentoXMovimientoId": documentoXMovimientoId})
        elif f"El registro de auditoria con ese documento x movimiento Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"documentoXMovimientoId": documentoXMovimientoId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})


async def completarAuditoriaUsuario(
        usuarioId:int,
        usuarioResponsableId:int,
        headerData:dict,
        db,
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:

        data = {
        "p_usuario_id": usuarioId,
        "p_ip_address": headerData['ipAddress'],
        "p_host_name": headerData['host'],
        "p_user_agent": headerData['userAgent'],
        "p_usuario_responsable_id": usuarioResponsableId
    }
        auditoriaResulList = await realizarConexionBD("completarUsuarioAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioResponsableId": usuarioResponsableId})
        elif f"El usuario Id no existe" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioId": usuarioId})
        elif f"El registro de auditoria con ese usuario Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"usuarioId": usuarioId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})
    

async def completarAuditoriaNotificacion(
        notificacionId:int,
        usuarioId:int,
        headerData:dict,
        db,
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:
        data = {
        "p_notificacion_id": notificacionId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioId,
    }
        auditoriaResulList = await realizarConexionBD("completarNotificacionAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioId": usuarioId})
        elif f"El notificacion Id no existe" in str(e):
            raise ServiceException(404, "Notificacion no encontrado", extra={"notificacionId": notificacionId})
        elif f"El registro de auditoria con ese notificacion Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"notificacionId": notificacionId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})

async def completarAuditoriaPermiso(
        permisoId:int,
        usuarioFisicoId:int,
        headerData:dict,
        db
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:
        data = {
        "p_permiso_id": permisoId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
    }
        auditoriaResulList = await realizarConexionBD("completarPermisoAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId})
        elif f"El permiso Id no existe" in str(e):
            raise ServiceException(404, "Permiso no encontrado", extra={"permisoId": permisoId})
        elif f"El registro de auditoria con ese permiso Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"permisoId": permisoId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})
    
async def completarAuditoriaRolXPermiso(
        rolXPermisoId:int,
        usuarioFisicoId:int,
        headerData:dict,
        db
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:
        data = {
        "p_rol_x_permiso_id": rolXPermisoId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
    }
        auditoriaResulList = await realizarConexionBD("completarRolXPermisoAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId})
        elif f"El rol x permiso Id no existe" in str(e):
            raise ServiceException(404, "Rol x permiso no encontrado", extra={"rolXPermisoId": rolXPermisoId})
        elif f"El registro de auditoria con ese rol x permiso Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"rolXPermisoId": rolXPermisoId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})
    
async def completarAuditoriaRol(
        rolId:int,
        usuarioFisicoId:int,
        headerData:dict,
        db
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:
        data = {
        "p_rol_id": rolId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
    }
        auditoriaResulList = await realizarConexionBD("completarRolAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId})
        elif f"El rol Id no existe" in str(e):
            raise ServiceException(404, "Rol no encontrado", extra={"rolId": rolId})
        elif f"El registro de auditoria con ese rol Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"rolId": rolId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})

async def completarAuditoriaRolXUsuario(
        rolXUsuarioId:int,
        usuarioFisicoId:int,
        headerData:dict,
        db
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:
        data = {
        "p_rol_x_usuario_id": rolXUsuarioId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
    }
        auditoriaResulList = await realizarConexionBD("completarRolXUsuarioAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId})
        elif f"El rol x usuario Id no existe" in str(e):
            raise ServiceException(404, "Rol x usuario no encontrado", extra={"rolXUsuarioId": rolXUsuarioId})
        elif f"El registro de auditoria con ese rol x usuario Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"rolXUsuarioId": rolXUsuarioId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})


async def completarAuditoriaUsuarioGateway(
        usuarioId:int,
        usuarioFisicoId:int,
        headerData:dict,
        db
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """
    
    try:
        data = {
        "p_usuario_id": usuarioId,
        "p_ip_address": headerData["ipAddress"],
        "p_host_name": headerData["host"],
        "p_user_agent": headerData["userAgent"],
        "p_usuario_responsable_id": usuarioFisicoId,
        "p_usuario_aplicacion_responsable_id": 0,
        }
        auditoriaResulList = await realizarConexionBD("completarUsuarioGatewayAuditoria", data, db,keep=True)

        auditoriaResult= auditoriaResulList["rows"][0]
        return auditoriaResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId})
        elif f"El usuario Id no existe" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioId": usuarioId})
        elif f"El registro de auditoria con ese usuario Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"usuarioId": usuarioId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})


async def completarAuditoriaRolXUsuarioGateWay(
        usuarioId: int,
        usuarioFisicoId: int,
        headerData: dict,
        db
):
    """
    Completa la auditoria en la base de datos llamando un procedimiento almacenado
    """

    try:
        data = {
            "p_usuario_id": usuarioId,
            "p_ip_address": headerData["ipAddress"],
            "p_host_name": headerData["host"],
            "p_user_agent": headerData["userAgent"],
            "p_usuario_responsable_id": usuarioFisicoId,
            "p_usuario_aplicacion_responsable_id": 0,
        }
        auditoriaResulList = await realizarConexionBD("completarRolXUsuarioGatewayAuditoria", data, db, keep=True)

        auditoriaResult = auditoriaResulList["rows"][0]
        return auditoriaResult
    except ServiceException as e:
        raise e

    except Exception as e:
        if f"El usuario responsable no existe en la tabla de usuarios" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioFisicoId": usuarioFisicoId})
        elif f"El usuario Id no existe" in str(e):
            raise ServiceException(404, "Usuario no encontrado", extra={"usuarioId": usuarioId})
        elif f"El registro de auditoria con ese usuario Id no existe" in str(e):
            raise ServiceException(404, "Registro de auditoria no encontrado", extra={"usuarioId": usuarioId})
        else:
            raise ServiceException(500, "Error al completar la auditoría", extra={"message": str(e)})