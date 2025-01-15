from db.databaseUtils import realizarConexionBD
from schemes.rolScheme import rolCreate, rolResponse
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from db.models.rol import Rol

async def obtenerRolPorNombre(rolNombre: str, db) -> Rol:
    """
    parámetros:
        - rolNombre: str

    retorna:
        - rolResponse

    Exepciones:
        - ServiceException(404, "El rol solicitado no existe", extra={"rol_nombre": rolNombre})
        - ServiceException(404, "El rol solicitado se encuentra inactivo", extra={"rol_nombre": rolNombre})
        - ServiceException(500, "Error al obtener el rol", extra={"error": str(e), "rol_nombre": rolNombre})
    """
    try:
        params = {
            "p_nombre_rol": rolNombre
        }

        rolResultList = await realizarConexionBD(procNombre="obtenerRolPorNombre",
                                                  procParams=params,
                                                  db=db,
                                                  model=Rol)
        
        rolResult = rolResultList["rows"]

        if not rolResult:
            raise ServiceException(status_code=404, detail="El rol solicitado no existe", extra={"rol_nombre": rolNombre})
        
        rolResult = rolResult[0]

        if not verificarHash(rolResult, Rol, rolResult.hashTabla):
            raise ServiceException(status_code=500, detail="El hash del rol no coincide", extra={"rol_nombre": rolNombre})
        
        return rolResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"No existe un rol con el nombre" in str(e):
            raise ServiceException(status_code=404, detail="El rol solicitado no existe", extra={"rol_nombre": rolNombre})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el rol", extra={"error": str(e), "rol_nombre": rolNombre})


async def obtenerRolPorId(rolId: int, db) -> Rol:
    """
    parámetros:
        - rolId: int

    retorna:
        - rolResponse

    Exepciones:
        - ServiceException(404, "El rol solicitado no existe", extra={"rol_id": rolId})
        - ServiceException(404, "El rol solicitado se encuentra inactivo", extra={"rol_id": rolId})
        - ServiceException(500, "Error al obtener el rol", extra={"error": str(e), "rol_id": rolId})
    """
    try:
        params = {
            "p_rol_id": rolId
        }

        rolResultList = await realizarConexionBD(procNombre="obtenerRolPorId",
                                                  procParams=params,
                                                  db=db,
                                                  model=Rol)
        
        rolResult = rolResultList["rows"]

        if not rolResult:
            raise ServiceException(status_code=404, detail="El rol solicitado no existe", extra={"rol_id": rolId})
        
        rolResult = rolResult[0]

        if not verificarHash(rolResult, Rol, rolResult.hashTabla):
            raise ServiceException(status_code=500, detail="El hash del rol no coincide", extra={"rol_id": rolId})
        
        return rolResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"No existe un rol con el id" in str(e):
            raise ServiceException(status_code=404, detail="El rol solicitado no existe", extra={"rol_id": rolId})
        elif f"Se encuentra inactivo el rol con el id" in str(e):
            raise ServiceException(status_code=404, detail="El rol solicitado se encuentra inactivo", extra={"rol_id": rolId})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el rol", extra={"error": str(e), "rol_id": rolId})
        
async def obtenerRoles(db, skip=0, limit=10) -> list[Rol]:
    """
    parámetros:
        - db: Session

    retorna:
        - list[rolResponse]

    Exepciones:
        - ServiceException(500, "Error al obtener la lista de roles", extra={"error": str(e)})
    """
    try:
        params = {
            "p_skip": skip,
            "p_limit": limit
        }

        rolesResultList = await realizarConexionBD(procNombre="obtenerRoles",
                                                    procParams=params,
                                                    db=db,
                                                    model=Rol)
        
        rolesResult = rolesResultList["rows"]

        result = []
        for rol in rolesResult:
            if not verificarHash(rol, Rol, rol.hashTabla):
                raise ServiceException(status_code=500, detail="El hash del rol no coincide", extra={"rol_id": rol.rolId})

            result.append({
                "rolId": rol.rolId,
                "nombreRol": rol.nombreRol,
                "descripcionRol": rol.descripcionRol,
                "fechaCreacion": rol.fechaCreacion,
                "activo": rol.activo,
                "hashTabla": rol.hashTabla
            })

        result.sort(key=lambda x: x["rolId"])

        return result
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al obtener la lista de roles", extra={"error": str(e)})