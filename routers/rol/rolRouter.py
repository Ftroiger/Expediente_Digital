from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from schemes.rolScheme import rolCreate, rolResponse
from db.database import get_db
from servicios.compartido.auditoria.completarAuditoria import completarAuditoriaRol, completarAuditoriaRolXPermiso, completarAuditoriaRolXUsuario
from servicios.compartido.obtenerDatosAuditoria import obtenerAuditoriaHeader
from servicios.compartido.verificarEstadoActivo import verificarEstadoActivo
from servicios.permisos.permisoMiddleware import verificarPermisoUsuario
from utils.error.errors import ServiceException
import logging
from servicios.compartido.rol.crearRoles import crearRol
from servicios.compartido.rol.obtenerRoles import obtenerRolPorId, obtenerRoles
from servicios.compartido.rol.eliminarRoles import eliminarRolPorNombre
from schemes.rolXPermisoScheme import RolXPermisoCreate, RolXPermisoResponse, PermisosPorRolResponse
from servicios.compartido.rolXPermiso.obtenerRolXPermiso import crearRolXPermiso, obtenerRolXPermiso, obtenerRolXPermisoPorNombreRol

# Configurar el logging
logger = logging.getLogger("Expediente")

router = APIRouter()

# POST: Crear un nuevo rol
@router.post("",
             response_model=rolResponse,
             summary="Crear un nuevo rol",
             description="Crea un nuevo rol en la base de datos")
async def postRol(request: Request, rol: rolCreate, db: Session = Depends(get_db)):
    try:
        datosAuditoria = obtenerAuditoriaHeader(request)

        usuarioId = request.headers.get("X-Usuario-Id")

        await verificarPermisoUsuario(usuarioId, ["Crear Rol"], db)
        rol = await crearRol(rol, db)
        await completarAuditoriaRol(
            rolId = rol.rolId,
            usuarioFisicoId = usuarioId,
            headerData = datosAuditoria,
            db=db
        )
        db.commit()
        return rolResponse.model_validate(rol)
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        return ServiceException(status_code=500, detail="Error al crear el rol", extra={"error": str(e)})

@router.post("/rolXpermiso",
             response_model=RolXPermisoResponse,
             summary="Crear un rol con permiso",
             description="Crea un rol con un permiso en la base de datos")
async def postRolXPermiso(request: Request, rolXPermiso: RolXPermisoCreate, db: Session = Depends(get_db)):
    try:
        dataAuditoria = obtenerAuditoriaHeader(request)

        db.begin()
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Crear rol con permiso"], db)
        rolXPermiso = await crearRolXPermiso(rolXPermiso, db)
        await completarAuditoriaRolXPermiso(
            rolXPermisoId = rolXPermiso.rolXPermisoId,
            usuarioFisicoId = usuarioId,
            headerData = dataAuditoria,
            db=db
        )
        
        
        db.commit()
        return rolXPermiso
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        return ServiceException(status_code=500, detail="Error al crear el rol con permiso", extra={"error": str(e)})

@router.get("/rolXpermiso",
            response_model=List[RolXPermisoResponse],
            summary="Obtener roles con permisos",
            description="Obtiene una lista de roles con sus permisos")
async def getRolesXPermiso(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise ServiceException(status_code=400, detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a cero", extra={"skip": skip, "limit": limit})
    
    try:
        usuarioId = request.headers.get("X-Usuario-Id")
        # ---- PERMISOS ---- #
        await verificarPermisoUsuario(usuarioId, ["Auditar"], db)
        roles = await obtenerRolXPermiso(db, skip=skip, limit=limit)
        return roles
    
    except ServiceException as e:
        raise e
    except Exception as e:
        return ServiceException(status_code=500, detail="Error al obtener la lista de roles con permisos", extra={"error": str(e)})

@router.get("/permisoPorRol/{nombreRol}",
            response_model=List[PermisosPorRolResponse],
            summary="Obtener permisos por rol",
            description="Obtiene una lista de permisos por rol")
async def getPermisosPorRol(request: Request, nombreRol: str, db: Session = Depends(get_db)):
    try:
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Auditar"], db)
        roles = await obtenerRolXPermisoPorNombreRol(db, nombreRol)
        return roles
    
    except ServiceException as e:
        raise e
    except Exception as e:
        return ServiceException(status_code=500, detail="Error al obtener la lista de permisos por rol", extra={"error": str(e)})
    
# GET: Obtener rol por Id
@router.get("/{rolId}",
            response_model=rolResponse,
            summary="Obtener rol por Id",
            description="Obtiene un rol por su Id")
async def getRolById(request: Request, rolId: int, db: Session = Depends(get_db)):
    try:
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Auditar"], db)
        rol = await obtenerRolPorId(rolId, db)
        logger.debug("Rol obtenido exitosamente por id")
        return rolResponse.model_validate(rol)
    except ServiceException as e:
        raise e
    except Exception as e:
        return ServiceException(status_code=500, detail="Error al obtener el rol", extra={"error": str(e)})
    
# GET: Obtener todos los roles
@router.get("",
            response_model=List[rolResponse],
            summary="Obtener todos los roles",
            description="Obtiene una lista de todos los roles registrados")
async def getRoles(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise ServiceException(status_code=400, detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a cero", extra={"skip": skip, "limit": limit})
    
    try:
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Auditar"], db)
        roles = await obtenerRoles(db, skip=skip, limit=limit)
        
        # Filtrar los roles por estado activo
        rolesActivos = verificarEstadoActivo(roles)
        logger.debug("Lista de roles obtenida exitosamente")
        return rolesActivos  # Ya es compatible con rolResponse
    
    except ServiceException as e:
        raise e
    except Exception as e:
        return ServiceException(status_code=500, detail="Error al obtener la lista de roles", extra={"error": str(e)})
    
# DELETE: Eliminar un rol por nombre
@router.delete("/{nombreRol}",
            response_model=bool,
            summary="Eliminar rol por nombre",
            description="Elimina un rol por su nombre")
async def deleteRol(request: Request, nombreRol: str, db: Session = Depends(get_db)):
    try:

        #Obtener datos Auditoria
        datosAuditoria = obtenerAuditoriaHeader(request)
        #Verificar Permisos
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Eliminar Rol"], db)
        
        #Cambiar guion por espacio en blanco
        nombreRol= nombreRol.replace("-", " ")
        resultado = await eliminarRolPorNombre(nombreRol, db)

        #Completar Auditoria
        rol = resultado["rol"]
        await completarAuditoriaRol(
            rolId = rol["rolId"],
            usuarioFisicoId = usuarioId,
            headerData = datosAuditoria,
            db=db
        )
        for rolXPermiso in resultado["rolXPermiso"]:
            await completarAuditoriaRolXPermiso(
                rolXPermisoId = rolXPermiso["rolXPermisoId"],
                usuarioFisicoId = usuarioId,
                headerData = datosAuditoria,
                db=db
            )

        db.commit()
        
        logger.debug("Rol eliminado exitosamente")
        return resultado["eliminarRolPorNombre"]
    except ServiceException as e:
        raise e
    except Exception as e:
        return ServiceException(status_code=500, detail="Error al eliminar el rol", extra={"error": str(e), "nombreRol": nombreRol})
    