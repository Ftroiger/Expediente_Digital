from fastapi import Request
from db.databaseUtils import realizarConexionBD
from db.models.usuario import Usuario
from schemes.usuarioScheme import UsuarioAplicacionCreate, UsuarioAdministradorCreate, UsuarioCreate, UsuarioSuperAdminCreate
from utils.error.errors import ServiceException
from utils.hash.apiKeyGen import generarApiKey

# Función que inserta un Usuario Aplicación en la base de datos
async def insertarUsuarioAplicacion(usuarioAplicacion: UsuarioAplicacionCreate, usuarioAltaId, db) -> Usuario:
    """
    Parámetros:
        - usuarioAplicacion: UsuarioAplicacionCreate

    Retorna:
        - Usuario

    Excepciones:
        - ServiceException(500, "Error al insertar el usuario", extra={"error": str(e)})
    """
    try:
        # Generar la apiKey
        apiKey = generarApiKey()

        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_usuario_alta_id": usuarioAltaId,
            "p_nombre_usuario": usuarioAplicacion.nombreUsuario,
            "p_area_id": usuarioAplicacion.areaId,
            "p_aplicacion_vedi_id": usuarioAplicacion.aplicacionVediId,
            "p_api_key": apiKey
        }

        usuarioResultDict = await realizarConexionBD("crearUsuarioAplicacion", params, db, model=Usuario)

        usuarioResult = usuarioResultDict["rows"][0]

        return usuarioResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"El sistema vertical ya posee una aplicación asociada" in str(e):
            raise ServiceException(404, "El sistema vertical ya posee una aplicación asociada", extra={"nombre_usuario": usuarioAplicacion.nombreUsuario, "area_id": usuarioAplicacion.areaId, "aplicacion_vedi_id": usuarioAplicacion.aplicacionVediId})
        elif f"No se encontró el rol Usuario Aplicacion" in str(e):
            raise ServiceException(404, "No se encontró el rol Usuario Aplicacion", extra={"nombre_usuario": usuarioAplicacion.nombreUsuario, "area_id": usuarioAplicacion.areaId, "aplicacion_vedi_id": usuarioAplicacion.aplicacionVediId})
        else:
            raise ServiceException(500, "Error al insertar el usuario", extra={"error": str(e)})

# Función que inserta un Administrador en la base de datos
async def insertarAdministrador(usuarioAlta: int, administrador: UsuarioAdministradorCreate, db) -> Usuario:
    """
    Parámetros:
        - administrador: UsuarioAplicacionCreate

    Retorna:
        - Usuario

    Excepciones:
        - ServiceException(500, "Error al insertar el administrador", extra={"error": str(e)})
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_cuil_usuario": administrador.cuilUsuario,
            "p_nombre_usuario": administrador.nombreUsuario,
            "p_area_id": administrador.areaId,
            "p_usuario_alta": usuarioAlta
        }
        administradorResultDict = await realizarConexionBD("crearUsuarioAdministrador", params, db, model=Usuario)
        administradorResult = administradorResultDict["rows"][0]
        return administradorResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"El usuario ya existe" in str(e):
            raise ServiceException(404, "El usuario ya existe", extra={"nombre_usuario": administrador.nombreUsuario, "cuil_usuario": administrador.cuilUsuario, "area_id": administrador.areaId, "aplicacion_vedi_id": administrador.aplicacionVediId})
        else:
            raise ServiceException(500, "Error al insertar el administrador", extra={"error": str(e)})
        
async def insertarSuperAdmin(usuarioAlta:int,superAdmin: UsuarioSuperAdminCreate, db) -> Usuario:
    """
    params:
        - superAdmin: UsuarioSuperAdminCreate

    return:
        - Usuario

    exceptions:
        - ServiceException(500, "Error al insertar el super administrador", extra={"error": str(e)})
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_cuil_usuario": superAdmin.cuilUsuario,
            "p_nombre_usuario": superAdmin.nombreUsuario,
            "p_area_id": superAdmin.areaId,
            "p_usuario_alta": usuarioAlta
        }

        superAdminResultDict = await realizarConexionBD("crearUsuarioSuperAdmin", params, db, model=Usuario)
        superAdminResult = superAdminResultDict["rows"][0]

        return superAdminResult
    
    except ServiceException as e:
        raise e

    except Exception as e:
        if f"El usuario ya existe" in str(e):
            raise ServiceException(404, "El usuario ya existe", extra={"nombre_usuario": superAdmin.nombreUsuario, "cuil_usuario": superAdmin.cuilUsuario, "area_id": superAdmin.areaId})
        else:
            raise ServiceException(500, "Error al insertar el super administrador", extra={"error": str(e)})
        

# Funcion para insertar un usuario en la base de datos
async def insertarUsuario(usuarioAltaId: int, usuario: UsuarioCreate, rolUsuarioId: int, db) -> Usuario:
    """
    Función general para insertar un usuario en la base de datos, predefiniendo el rol del usuario.

    Parámetros:
        - usuarioAltaId: int
        - usuario: UsuarioCreate
        - rolUsuarioId: int
        - db: Base de datos

    Retorna:
        - Usuario
    
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_nombre_usuario": usuario.nombreUsuario,
            "p_cuil_usuario": usuario.cuilUsuario,
            "p_area_id": usuario.areaId,
            "p_usuario_alta": usuarioAltaId,
            "p_rol_usuario_id": rolUsuarioId
        }

        usuarioResultDict = await realizarConexionBD("crearUsuario", params, db, model=Usuario)
        usuarioResult = usuarioResultDict["rows"][0]

        return usuarioResult
    
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al insertar el usuario", extra={"error": str(e)})