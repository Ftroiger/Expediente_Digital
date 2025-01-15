from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic_core import ValidationError
from typing import List
from db.database import get_db
from schemes.notificacionScheme import NotificacionResponse
from schemes.usuarioScheme import UsuarioAdministradorCreate, UsuarioAplicacionCreate, UsuarioAplicacionResponse, UsuarioNotificacionCreate, UsuarioResponse, UsuarioCreate
from schemes.usuarioScheme import UsuarioAdministradorCreate, UsuarioAplicacionCreate, UsuarioAplicacionResponse, UsuarioResponse, UsuarioCreate, UsuarioSuperAdminCreate
from schemes.permisoScheme import PermisoResponse
from servicios.baseUnica.apiBaseUnica import getDependenciaById
from servicios.compartido.verificarEstadoActivo import verificarEstadoActivo
from servicios.compartido.obtenerDatosAuditoria import obtenerAuditoriaHeader
from servicios.compartido.auditoria.completarAuditoria import completarAuditoriaRolXUsuario, completarAuditoriaUsuario, completarAuditoriaNotificacion
from servicios.compartido.usuario.obtenerUsuario import obtenerUsuarioPorId, obtenerUsuarios
from servicios.compartido.usuario.darBajaUsuario import darBajaUsuario, pedidoDarBajaUsuarioAplicacion
from servicios.compartido.usuario.revocarRolUsuario import revocarRolUsuario
from servicios.compartido.usuario.obtenerUsuario import verificarExistenciaUsuario, verificarExistenciaUsuarioAplicacion
from servicios.compartido.usuario.insertarUsuarioBdd import insertarUsuarioAplicacion, insertarAdministrador, insertarSuperAdmin
from servicios.permisos.permisoMiddleware import verificarPermisoUsuario
from utils.error.errors import ErrorResponse, ServiceException

router = APIRouter()

@router.post(
    "/usuario/superAdmin",
    tags=["Usuarios"],
    response_model=UsuarioResponse,
    summary="Crear un nuevo usuario",
    description="Permite crear un usuario.",
)
async def createSuperAdmin(request: Request, usuario: UsuarioSuperAdminCreate, db: Session = Depends(get_db)):
    try:
        dataAuditoria = obtenerAuditoriaHeader(request)
        usuarioId = request.headers.get("X-Usuario-Id")

        db.begin()
        # ---- PERMISOS
        # Usuarios con rol super admin pueden crear usuarios con rol super admin
        await verificarPermisoUsuario(usuarioId, ["Crear Super Admin"], db)

        # ---- VALIDAR EXISTENCIA AREA
        await getDependenciaById(usuario.areaId)

        # ---- USUARIO
        # Crear el usuario
        usuarioResult = await insertarSuperAdmin(usuarioId,usuario, db)
        # ---- Actualizar la auditoria
        await completarAuditoriaUsuario(
            usuarioResult.usuarioId, 
            usuarioId,
            dataAuditoria,
            db
        )        

        db.commit()
        return usuarioResult
    
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc

@router.get("/usuario",
            tags=["Usuarios"],
            response_model=List[UsuarioResponse],
            summary="Consultar los usuarios",
            description="Obtiene la lista de usuarios.",
)
async def getUsuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Validación de los parámetros 'skip' y 'limit'
    if skip < 0 or limit < 1:
        raise ServiceException(status_code=400, detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a cero", extra={"skip": skip, "limit": limit})
    
    try:
        # Consulta a la base de datos con paginación
        usuarios = await obtenerUsuarios(db, skip, limit)
        if not usuarios:
            raise ServiceException(status_code=404, detail="No se encontraron usuarios")

        # Filtrar los usuarios por estado activo

        usuariosActivos = verificarEstadoActivo(usuarios)
        
        # Verificación de si se encontraron expedientes
        
                
        return usuariosActivos
    
    except SQLAlchemyError as e:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ValidationError as e:
        db.rollback()
        raise e
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc
        
# Crear un usuario administrador
@router.post(
    "/usuario/administrador",
    tags=["Usuarios"],
    response_model=UsuarioResponse,
    summary="Crear un nuevo usuario administrador",
    description="Permite crear un usuario asignándole el rol administrador.",
)
async def createUsuarioAdministrador(request: Request, usuario: UsuarioAdministradorCreate, db: Session = Depends(get_db)):
    try:
        dataAuditoria = obtenerAuditoriaHeader(request)
        usuarioId = request.headers.get("X-Usuario-Id")

        db.begin()
        # ---- PERMISOS
        # Usuarios con rol super admin pueden crear usuarios con rol administrador
        await verificarPermisoUsuario(usuarioId, ["Crear Administrador"], db)

        # ---- VALIDAR EXISTENCIA AREA
        await getDependenciaById(usuario.areaId)

        # ---- USUARIO
        # Crear el usuario
        usuarioResult = await insertarAdministrador(usuarioId, usuario, db)

        # ---- Actualizar la auditoria
        await completarAuditoriaUsuario(
            usuarioResult.usuarioId,
            usuarioId,
            dataAuditoria,
            db
        )
        # ---- COMMIT
        db.commit()
        return usuarioResult

    except ServiceException as e:
        db.rollback()
        raise e
    except SQLAlchemyError as e:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ValidationError as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc

# Obtener un usuario por su id
@router.get(
    "/usuario/{usuarioId}",
    tags=["Usuarios"],
    response_model=UsuarioResponse,
    summary="Obtener un usuario por su id",
    description="Permite obtener un usuario por su id.",
)
async def getUsuarioById(request: Request, usuarioId: int, db: Session = Depends(get_db)):
    try:
        usuarioAdminId = request.headers.get("X-Usuario-Id")

        # Obtener el usuario
        usuarioAplicacion = await obtenerUsuarioPorId(usuarioId, db)

        # Verificar si se encontró el usuario
        if not usuarioAplicacion:
            raise ServiceException(status_code=404, detail="Usuario no encontrado", extra={"usuario_id": usuarioId})

        # Verificar si el usuario tiene permiso para acceder al usuario
        if not usuarioAdminId == usuarioAplicacion.usuarioAlta:
            raise ServiceException(status_code=400, detail="No tiene permisos para acceder a este usuario", extra={"usuarioId": usuarioId})
        

        return usuarioAplicacion

    except ServiceException as e:
        db.rollback()
        raise e
    except SQLAlchemyError as e:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ValidationError as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc

# Endpoint para crear un sistema vertical
@router.post(
    "/usuario/aplicacion",
    tags=["Usuarios"],
    response_model=UsuarioAplicacionResponse,
    summary="Crear un nuevo usuario aplicacion",
    description="Permite crear un usuario asignándole el rol aplicación (sistema vertical).",
)
async def crearUsuarioAplicacion(request: Request, usuario: UsuarioAplicacionCreate, db: Session = Depends(get_db)):
    try:
        dataAuditoria = obtenerAuditoriaHeader(request)
        usuarioId = request.headers.get("X-Usuario-Id")

        db.begin()

        # ---- PERMISOS
        # Usuarios con rol administrador pueden crear usuarios con rol aplicación
        await verificarPermisoUsuario(usuarioId, ["Dar de alta Sistema Vertical"], db)

        # ---- VALIDAR EXISTENCIA AREA
        await getDependenciaById(usuario.areaId)

        # ---- USUARIO
        # Crear el usuario
        usuarioResult = await insertarUsuarioAplicacion(usuario, usuarioId, db)

        # ---- Actualizar la auditoria
        await completarAuditoriaUsuario(
            usuarioResult.usuarioId,
            usuarioId,
            dataAuditoria,
            db
        )

        db.commit()
        return usuarioResult

    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


# Endpoint para pedido dar de baja un sismtema vertical
@router.delete(
    "/usuario/{usuarioAplicacionId}/pedidoBaja",
    tags=["Usuarios"],
    response_model=NotificacionResponse,
    summary="Dar de baja un usuario",
    description="Permite dar de baja un usuario.",
)
async def pedidoDarDeBajaUsuarioAplicacion(request: Request, notificacion: UsuarioNotificacionCreate, usuarioAplicacionId: int, db: Session = Depends(get_db)):
    try:
        db.begin()

        dataAuditoria = obtenerAuditoriaHeader(request)
        # ---- PERMISOS
        usuarioId = request.headers.get("X-Usuario-Id")


        # Verificar si el usuario tiene permiso para dar de baja
        await verificarPermisoUsuario(usuarioId, ["Pedido dar de baja Sistema Vertical"], db)

        usuarioAplicacion = await obtenerUsuarioPorId(usuarioAplicacionId, db)

        # Verificar si el altaUsuario del usuarioAplicacion corresponde al admin
        if int(usuarioAplicacion.usuarioAlta) != int(usuarioId):
            raise ServiceException(status_code=403, detail="El usuario que solicita la baja no es el mismo que dio de alta al sistema vertical.", extra={"usuario_id": usuarioId, "usuario_alta": usuarioAplicacion.usuarioAlta})

        # ---- NOTIFICACION PARA DAR DE BAJA
        # Notificar al usuario que se ha pedido dar de baja
        notificacionBaja = await pedidoDarBajaUsuarioAplicacion(usuarioId, usuarioAplicacionId, notificacion.descripcionNotificacion, db)

        # ---- Actualizar Auditori
        await completarAuditoriaNotificacion(
            notificacionBaja.notificacionId,
            usuarioId,
            dataAuditoria,
            db
        )

        # ---- COMMIT
        db.commit()

        return notificacionBaja

    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


# Endpoint para dar de baja un sistema vertical
@router.delete(
    "/usuario/{usuarioAplicacionId}/baja",
    tags=["Usuarios"],
    response_model=UsuarioResponse,
    summary="Dar de baja un usuario",
    description="Permite dar de baja un usuario.",
)
async def darDeBajaUsuarioAplicacion(request: Request, usuarioAplicacionId: int, db: Session = Depends(get_db)):
    try:
        db.begin()

        # ---- PERMISOS
        usuarioId = request.headers.get("X-Usuario-Id")

        await verificarPermisoUsuario(usuarioId, ["Dar de baja Sistema Vertical"], db)

        # ---- USUARIO
        # Dar de baja el usuario
        usuarioAplicacion = await darBajaUsuario(usuarioAplicacionId, db)

        # ---- COMMIT
        db.commit()
        return usuarioAplicacion

    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


# Endpoint para revocar el rol a un usuario
@router.delete(
    "/usuario/{usuarioId}/rol",
    tags=["Usuarios"],
    response_model=bool,
    summary="Revocar el rol a un usuario",
    description="Permite revocar el rol a un usuario.",
)
async def revocarRolXUsuario(request: Request, usuarioId: int, db: Session = Depends(get_db)):
    try:
        dataAuditoria = obtenerAuditoriaHeader(request)

        db.begin()

        # ---- PERMISOS
        usuarioAdminId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioAdminId, ["Cambiar rol Usuario"], db)

        # ---- USUARIO
        # Revocar el rol al usuario actual por el de usuario fisico
        rolXUsuarioResult = await revocarRolUsuario(usuarioId, db)

        # ---- Actualizar la auditoria
        rolesXUsuariosEliminados = rolXUsuarioResult["rolesXUsuariosEliminados"]
        for rolXUsuarioEliminado in rolesXUsuariosEliminados:
            await completarAuditoriaRolXUsuario(
                rolXUsuarioEliminado.rolXUsuarioId,
                usuarioAdminId,
                dataAuditoria,
                db
            )
        rolXUsuarioCreado = rolXUsuarioResult["rolXUsuarioCreado"]
        await completarAuditoriaRolXUsuario(
            rolXUsuarioCreado.rolXUsuarioId,
            usuarioAdminId,
            dataAuditoria,
            db
        )
        # ---- COMMIT
        db.commit()
        return rolXUsuarioResult["eliminarRolDeUsuario"]

    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()