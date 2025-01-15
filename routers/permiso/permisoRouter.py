from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from schemes.permisoScheme import PermisoCreate, PermisoResponse
from db.database import get_db
from servicios.compartido.verificarEstadoActivo import verificarEstadoActivo
from servicios.compartido.auditoria.completarAuditoria import completarAuditoriaPermiso, completarAuditoriaRolXPermiso
from servicios.compartido.obtenerDatosAuditoria import obtenerAuditoriaHeader
from servicios.permisos.permisoMiddleware import verificarPermisoUsuario
from utils.error.errors import ServiceException
import logging
from servicios.compartido.permisos.obtenerPermisos import obtenerPermisoPorId, obtenerPermisos
from servicios.compartido.permisos.crearPermisos import crearPermiso
from servicios.compartido.permisos.eliminarPermisos import eliminarPermiso

# Configurar el logging
logger = logging.getLogger("Expediente")

router = APIRouter()

# POST: Crear un nuevo permiso
@router.post("",
             response_model=PermisoResponse,
             summary="Crear un nuevo permiso",
             description="Crea un nuevo permiso en la base de datos")
async def postPermiso(request: Request, permiso: PermisoCreate, db: Session = Depends(get_db)):
    try:
        datosAuditoria = obtenerAuditoriaHeader(request)
        db.begin()
        
        usuarioId = request.headers.get("X-Usuario-Id")
        
        await verificarPermisoUsuario(usuarioId, ["Crear Permiso"], db)
        
        permiso = await crearPermiso(permiso, db)
        await completarAuditoriaPermiso(
            permisoId = permiso['permisoId'],
            usuarioFisicoId = usuarioId,
            headerData = datosAuditoria,
            db=db
        )

        await completarAuditoriaRolXPermiso(
            rolXPermisoId = permiso['rolXPermiso']['rolXPermisoId'],
            usuarioFisicoId = usuarioId,
            headerData = datosAuditoria,
            db=db
        )
        db.commit()
        return permiso
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        return ServiceException(status_code=500, detail="Error al crear el permiso", extra={"error": str(e)})

# GET: Obtener todos los permisos
@router.get("",
            response_model=List[PermisoResponse],
            summary="Obtener todos los permisos",
            description="Obtiene una lista de todos los permisos registrados")
async def getPermiso(request: Request, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    if skip < 0 or limit < 1:
        raise ServiceException(status_code=400, detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a cero", extra={"skip": skip, "limit": limit})
    
    try:
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Auditar"], db)
        permisos = await obtenerPermisos(db, skip=skip, limit=limit)

        # Verificar que los permisos esten activos
        permisosActivos = verificarEstadoActivo(permisos)
        logger.debug("Lista de permisos obtenida exitosamente")
        return permisosActivos  # Ya es compatible con permisoResponse
    
    except ServiceException as e:
        raise e
    except Exception as e:
        return ServiceException(status_code=500, detail="Error al obtener la lista de permisos", extra={"error": str(e)})
    
# GET by ID: Obtener un permiso por ID
@router.get("/{idPermiso}",
            response_model=PermisoResponse,
            summary="Obtener permiso por ID",
            description="Obtiene un permiso específico por su ID")
async def getPermisoById(request: Request, idPermiso: int, db: Session = Depends(get_db)):
    try:
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Auditar"], db)
        permiso = await obtenerPermisoPorId(idPermiso, db)
        return PermisoResponse.model_validate(permiso)
    except ServiceException as e:
        raise e
    except Exception as e:
        return ServiceException(status_code=500, detail="Error al obtener el permiso", extra={"error": str(e), "permiso_id": idPermiso})

# DELETE: Eliminar un permiso por nombre
@router.delete("/{nombrePermiso}",
               response_model=bool,
               summary="Eliminar un permiso",
               description="Elimina un permiso específico por su nombre")
async def deletePermiso(request: Request, nombrePermiso: str, db: Session = Depends(get_db)):
    try:
        dataAuditoria = obtenerAuditoriaHeader(request)

        # Cambiar el - por espacio en blanco de nombrePermiso
        nombrePermiso = nombrePermiso.replace("-", " ")

        db.begin()
        
        usuarioId = request.headers.get("X-Usuario-Id")
        await verificarPermisoUsuario(usuarioId, ["Eliminar Permiso"], db)
        
        resultado = await eliminarPermiso(nombrePermiso, db)
        permiso = resultado['permiso']
        rolesXPermisos= resultado['rolXPermiso']

        #Completar las auditorias de Permiso y tabla pasarela
        await completarAuditoriaPermiso(
            permisoId = permiso['permisoid'],
            usuarioFisicoId = usuarioId,
            headerData = dataAuditoria,
            db=db
        )
        for rolxPermiso in rolesXPermisos:
            await completarAuditoriaRolXPermiso(
                rolXPermisoId = rolxPermiso['rolxpermisoid'],
                usuarioFisicoId = usuarioId,
                headerData = dataAuditoria,
                db=db
            )

        logger.debug(f"Permiso eliminado: {resultado}")
        
        resultado =  True
        
        db.commit()
        return resultado
    except ServiceException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise ServiceException(status_code=500, detail="Error al eliminar el permiso", extra={"error": str(e), "permiso_nombre": nombrePermiso})