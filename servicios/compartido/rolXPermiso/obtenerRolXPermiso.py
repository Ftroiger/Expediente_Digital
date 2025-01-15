from db.databaseUtils import realizarConexionBD
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from db.models.rolXPermiso import RolXPermiso
from schemes.rolXPermisoScheme import PermisosPorRolResponse, RolXPermisoCreate

async def crearRolXPermiso(rolXPermiso: RolXPermisoCreate, db) -> RolXPermiso:
    """
    parámetros:
        - db: Session
        - rolXPermiso: RolXPermiso

    retorna:
        - RolXPermiso

    Exepciones:
        - serviceExepction(500, "Error al crear el rolXPermiso", extra={"error": str(e)})
    """
    try:
        params = {
            "p_rol_id": rolXPermiso.rolId,
            "p_permiso_id": rolXPermiso.permisoId
        }

        rolXPermisoResultList = await realizarConexionBD(procNombre="crearRelacionRolPermiso",
                                                      procParams=params,
                                                      db=db,
                                                      model=RolXPermiso)
        
        rolXPermisoResult = rolXPermisoResultList["rows"][0]

        return rolXPermisoResult
    
    except ServiceException as e:
        raise e


    except Exception as e:
        if f"La relación entre el rol y el permiso ya existe" in str(e):
            raise ServiceException(status_code=400, detail="La relación entre el rol y el permiso ya existe", extra={"rolId": rolXPermiso.rolId, "permisoId": rolXPermiso.permisoId})
        elif f"El rol no existe" in str(e):
            raise ServiceException(status_code=400, detail="El rol no se encuentra", extra={"rolId": rolXPermiso.rolId})
        elif f"El permiso no existe" in str(e):
            raise ServiceException(status_code=400, detail="El permiso no se encuentra", extra={"permisoId": rolXPermiso.permisoId})
        else:
            raise ServiceException(status_code=500, detail="Error al crear el rolXPermiso", extra={"error": str(e)})

async def obtenerRolXPermiso(db, skip=0, limit=10) -> list[RolXPermiso]:
    """
    parámetros:
        - db: Session

    retorna:
        - list[rolXPermiso]

    Exepciones:
        - serviceExepction(500, "Error al obtener el rolXPermiso", extra={"error": str(e)})
    """
    try:
        params = {
            "p_skip": skip,
            "p_limit": limit
        }

        rolXPermisoResultList = await realizarConexionBD(procNombre="obtenerRolXPermiso",
                                                      procParams=params,
                                                      db=db,
                                                      model=RolXPermiso)
        
        rolXPermisoResult = rolXPermisoResultList["rows"]

        for rolXPermiso in rolXPermisoResult:
            if not verificarHash(rolXPermiso, RolXPermiso, rolXPermiso.hashTabla):
                raise ServiceException(status_code=500, detail="El hash del rolXPermiso no coincide")

        return rolXPermisoResult

    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al obtener el rolXPermiso", extra={"error": str(e)})
    
async def obtenerRolXPermisoPorNombreRol(db, nombreRol: int) -> list[PermisosPorRolResponse]:
    """
    parámetros:
        - db: Session
        - rolId: int

    retorna:
        - list[rolXPermiso]

    Exepciones:
        - serviceExepction(500, "Error al obtener el rolXPermiso", extra={"error": str(e)})
    """
    try:
        # eliminar guiones del nombre rol y reemplazar por un espacio
        nombreRol = nombreRol.replace("-", " ")
        
        params = {
            "p_nombre_rol": nombreRol
        }

        rolXPermisoResultList = await realizarConexionBD(procNombre="obtenerPermisosPorNombreRol",
                                                      procParams=params,
                                                      db=db)
        
        rolXPermisoResult = rolXPermisoResultList["rows"]


        return rolXPermisoResult

    except ServiceException as e:
        raise e
    except Exception as e:
        if f"El rol no existe" in str(e):
            raise ServiceException(status_code=400, detail="El rol no se encuentra registrado", extra={"nombreRol": nombreRol})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el rolXPermiso", extra={"error": str(e)})