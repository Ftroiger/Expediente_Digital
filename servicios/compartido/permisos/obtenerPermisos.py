from db.databaseUtils import realizarConexionBD
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from db.models.permiso import Permiso

async def obtenerPermisoPorId(permisoId: int, db) -> Permiso:
    """
    parámetros:
        - permisoId: int

    retorna:
        - permisoResponse

    Exepciones:
        - ServiceException(404, "El permiso solicitado no existe", extra={"permiso_id": permisoId})
        - ServiceException(404, "El permiso solicitado se encuentra inactivo", extra={"permiso_id": permisoId})
        - ServiceException(500, "Error al obtener el permiso", extra={"error": str(e), "permiso_id": permisoId})
    """
    try:
        params = {
            "p_permiso_id": permisoId
        }

        permisoResultList = await realizarConexionBD(procNombre="obtenerPermisoPorId",
                                                      procParams=params,
                                                      db=db,
                                                      model=Permiso)
        
        permisoResult = permisoResultList["rows"]

        if not permisoResult:
            raise ServiceException(status_code=404, detail="El permiso solicitado no existe", extra={"permiso_id": permisoId})
        
        permisoResult = permisoResult[0]

        if not verificarHash(permisoResult, Permiso, permisoResult.hashTabla):
            raise ServiceException(status_code=500, detail="El hash del permiso no coincide", extra={"permiso_id": permisoId})
        
        return permisoResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El permiso con id {permisoId} no existe" in str(e):
            raise ServiceException(status_code=404, detail="El permiso solicitado no existe", extra={"permiso_id": permisoId})
        elif f"El permiso con id {permisoId} no se encuentra activo" in str(e):
            raise ServiceException(status_code=404, detail="El permiso solicitado se encuentra inactivo", extra={"permiso_id": permisoId})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el permiso", extra={"error": str(e), "permiso_id": permisoId})
        
async def obtenerPermisos(db, skip=0, limit=10) -> list[Permiso]:
    """
    parámetros:
        - db: Session

    retorna:
        - list[permisoResponse]

    Exepciones:
        - ServiceException(500, "Error al obtener la lista de permisos")
    """
    try:
        params = {
            "p_skip": skip,
            "p_limit": limit
        }
        permisos = await realizarConexionBD(procNombre="obtenerPermisos",
                                            procParams=params,
                                            db=db,
                                            model=Permiso)

        permisosResult = permisos["rows"]

        # Validar hashes de cada permiso
        for permiso in permisosResult:
            if not verificarHash(permiso, Permiso, permiso.hashTabla):
                raise ServiceException(
                    status_code=500,
                    detail="El hash del permiso no coincide",
                    extra={"permiso_id": permiso.permisoId}
                )

        return permisosResult  # Devuelve directamente la lista de objetos Permiso
    
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al obtener la lista de permisos")
    
async def obtenerPermisoPorNombre (nombrePermiso: str, db) -> Permiso:
    """
    parámetros:
        - nombrePermiso: str

    retorna:
        - permisoResponse

    Exepciones:
        - ServiceException(404, "El permiso solicitado no existe", extra={"nombre_permiso": nombrePermiso})
        - ServiceException(404, "El permiso solicitado se encuentra inactivo", extra={"nombre_permiso": nombrePermiso})
        - ServiceException(500, "Error al obtener el permiso", extra={"error": str(e), "nombre_permiso": nombrePermiso})
    """
    try:
        params = {
            "p_nombre_permiso": nombrePermiso
        }

        permisoResultList = await realizarConexionBD(procNombre="obtenerPermisoPorNombre",
                                                      procParams=params,
                                                      db=db,
                                                      model=Permiso)
        
        permisoResult = permisoResultList["rows"]

        if not permisoResult:
            raise ServiceException(status_code=404, detail="El permiso solicitado no existe", extra={"nombre_permiso": nombrePermiso})
        
        permisoResult = permisoResult[0]

        if not verificarHash(permisoResult, Permiso, permisoResult.hashTabla):
            raise ServiceException(status_code=500, detail="El hash del permiso no coincide", extra={"nombre_permiso": nombrePermiso})
        
        return permisoResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"El permiso con nombre {nombrePermiso} no existe" in str(e):
            raise ServiceException(status_code=404, detail="El permiso solicitado no existe", extra={"nombre_permiso": nombrePermiso})
        elif f"El permiso con nombre {nombrePermiso} no se encuentra activo" in str(e):
            raise ServiceException(status_code=404, detail="El permiso solicitado se encuentra inactivo", extra={"nombre_permiso": nombrePermiso})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el permiso", extra={"error": str(e), "nombre_permiso": nombrePermiso})