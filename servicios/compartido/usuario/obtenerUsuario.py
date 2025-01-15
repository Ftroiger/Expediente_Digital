import logging
from db.databaseUtils import realizarConexionBD
from schemes.documentoScheme import DocumentoResponse
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from db.models.usuario import Usuario

#logger = logging.getLogger("expediente")
# Función que obtiene todos los usuarios
async def obtenerUsuarios(db, skip=0, limit=10) -> list[Usuario]: 
    """
    Parámetros:
        - db: Session

    Retorna:
        - list[UsuarioResponse]

    Excepciones:
        - ServiceException(500, "Error al obtener los usuarios", extra={"error": str(e)})
    """
    try:
        params = {
            "p_skip": skip,
            "p_limit": limit
        }
        # Obtener los usuarios
        usuariosResultList = await realizarConexionBD(
                                    procNombre="obtenerUsuarios", 
                                    procParams=params, 
                                    db=db, 
                                    model=Usuario)
        usuariosResult = usuariosResultList["rows"]

        # Verificación del hash
        for usuario in usuariosResult:
            if not verificarHash(usuario, Usuario, usuario.hashTabla):
                raise ServiceException(status_code=500, detail="El hash del usuario no coincide", extra={"usuario_id": usuario.usuarioId})


        return usuariosResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al obtener los usuarios", extra={"error": str(e)})

# Función que obtiene un documento por su id
async def obtenerUsuarioPorCuil(cuilUsuario: str, db) -> Usuario:
    """
    Parámetros:
        - cuilUsuario: str

    Retorna:
        - Usuario

    Excepciones:
        - ServiceException(404, "No se encuentra el usuario solicitado", extra={"cuilUsuario": cuilUsuario})
        - ServiceException(404, "El usuario solicitado se encuentra inactivo", extra={"cuilUsuario": cuilUsuario})
        - ServiceException(500, "Error al obtener el usuario", extra={"error": str(e), "cuilUsuario": cuilUsuario})
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_cuil_usuario": cuilUsuario
        }
        
        # Obtener el usuario
        usuarioResultList = await realizarConexionBD(procNombre="obtenerUsuarioPorCuil", procParams=params, db=db, model=Usuario)
        usuarioResult = usuarioResultList["rows"][0]

        # Verificación del hash
        #if not verificarHash(usuarioResult, Usuario, usuarioResult.hashTabla):
        #    raise ServiceException(status_code=500, detail="El hash del usuario no coincide", extra={"cuilUsuario": cuilUsuario})
        
        #logger.debug(f"Usuario obtenido por su cuil: {usuarioResult}")
        return usuarioResult
    
    except ServiceException as e:
        raise e

    except Exception as e:
        if "No existe un usuario con el cuil" in str(e):
            raise ServiceException(status_code=404, detail="No se encuentra el usuario solicitado", extra={"cuilUsuario": cuilUsuario})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el usuario", extra={"error": str(e), "cuilUsuario": cuilUsuario})
        

# Función que obtiene un usuario por su id
async def obtenerUsuarioPorId(usuarioId: int, db) -> Usuario:
    """
    Parámetros:
        - usuarioId: int

    Retorna:
        - Usuario

    Excepciones:
        - ServiceException(404, "No se encuentra el usuario solicitado", extra={"usuarioId": usuarioId})
        - ServiceException(404, "El usuario solicitado se encuentra inactivo", extra={"usuarioId": usuarioId})
        - ServiceException(500, "Error al obtener el usuario", extra={"error": str(e), "usuarioId": usuarioId})
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_usuario_id": usuarioId
        }
        
        # Obtener el usuario
        usuarioResultList = await realizarConexionBD(procNombre="obtenerUsuarioPorId", procParams=params, db=db, model=Usuario)
        usuarioResult = usuarioResultList["rows"][0]

        # Verificación del hash
        #if not verificarHash(usuarioResult, Usuario, usuarioResult.hashTabla):
        #    raise ServiceException(status_code=500, detail="El hash del usuario no coincide", extra={"usuarioId": usuarioId})
        #logger.debug(f"Usuario obtenido por su id: {usuarioResult}")
        return usuarioResult
    
    except ServiceException as e:
        raise e
    

    except Exception as e:
        if "No existe un usuario con el id" in str(e):
            raise ServiceException(status_code=404, detail="No se encuentra el usuario solicitado", extra={"usuarioId": usuarioId})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el usuario", extra={"error": str(e), "usuarioId": usuarioId})
        
# # Función que obtiene un usuario por su rol
# async def obtenerUsuariosPorRol(rolId: int, db) -> list[UsuarioXRolResponse]:
#     """
#     Parámetros:
#         - rolId: int

#     Retorna:
#         - List[Usuario]

#     Excepciones:
#         - ServiceException(404, "No se encontraron usuarios para el rol indicado", extra={"rol_id": rolId})
#         - ServiceException(500, "Error al obtener los usuarios por rol", extra={"error": str(e), "rol_id": rolId})
#     """
#     try:
#         # Parámetros para el procedimiento almacenado
#         params = {"p_rol_id": rolId}

#         # Realizar la consulta al procedimiento almacenado
#         usuariosResultList = await realizarConexionBD(procNombre="obtenerUsuariosRol", 
#                                                       procParams=params, 
#                                                       db=db, 
#                                                       model=UsuarioXRolResponse)

#         usuariosResult = usuariosResultList["rows"]

#         if not usuariosResult:
#             raise ServiceException(status_code=404, detail="No se encontraron usuarios para el rol indicado", extra={"rol_id": rolId})

#         return usuariosResult

#     except ServiceException as e:
#         raise e
#     except Exception as e:
#         raise ServiceException(status_code=500, detail="Error al obtener los usuarios por rol", extra={"error": str(e), "rol_id": rolId})
    



# Función para verificar la existencia de un aplicacion ID y apiKey
async def verificarExistenciaUsuarioAplicacion(usuarioId: int, apiKey: str, db) -> bool:
    """
    Verifica si existe una aplicación vertical on usuarioId y apiKey proporcionados en la base de datos.

    Parámetros:
        - usuarioAplicacionId (int): El ID del UsuarioAplicacion a verificar.
        - apiKey (str): La apiKey del UsuarioAplicacion a verificar.
        - db: Conexión a la base de datos.

    Retorna:
        - True si el UsuarioAplicacion existe.
        - False si el UsuarioAplicacion no existe.
    
    Excepciones:
        - ServiceException(500, "Error al verificar la existencia del UsuarioAplicacion", extra={"usuarioAplicacionId": usuarioAplicacionId, "apiKey": apiKey})
    """
    try:
        # Llamar a la función almacenada en la base de datos
        resultado = await realizarConexionBD(
            "verificarExistenciaUsuarioAplicacion",
            {"p_usuario_id": usuarioId, "p_api_key": apiKey},
            db,
            model=None,
            keep=True
        )

        # Acceder a los 'rows' del resultado
        rows = resultado.get("rows", [])

        # Verificar si hay datos en 'rows'
        if not rows:
            # No existe el usuario
            raise ServiceException(
                status_code=404,
                detail="No se encuentra el usuario solicitado",
                extra={"usuarioId": usuarioId, "apiKey": apiKey}
            )
        # Obtener el valor de 'existe'
        existe = rows[0]['existe']

        # Retornar el resultado
        return existe
    
    except ServiceException as e:
        raise e


    except Exception as e:
        if f"No existe un usuario con el usuarioId" in str(e):
            raise ServiceException(
                status_code=404,
                detail="No se encuentra el usuario solicitado",
                extra={"usuarioId": usuarioId, "apiKey": apiKey}
            )
        elif f"La API Key no se encuentra válida" in str(e):
            raise ServiceException(
                status_code=401,
                detail="Sistema vertical no autorizado. Credenciales inválidas",
                extra={"usuarioId": usuarioId, "apiKey": apiKey}
            )
        elif f"El usuario se encuentra inactivo" in str(e):
            raise ServiceException(
                status_code=401,
                detail="El usuario se encuentra inactivo. Por favor, contacte al administrador",
                extra={"usuarioId": usuarioId, "apiKey": apiKey}
            )
        elif f"El usuario no está asociado a una aplicación" in str(e):
            raise ServiceException(
                status_code=401,
                detail="El usuario no está asociado a una aplicación",
                extra={"usuarioId": usuarioId, "apiKey": apiKey}
            )
        else:
            raise ServiceException(
                status_code=500,
                detail="Error al verificar la existencia del Usuario",
                extra={"error": str(e), "usuarioId": usuarioId, "apiKey": apiKey}
            )
    

# Función para verificar la existencia de un usuario
async def verificarExistenciaUsuario(usuarioId: int, db) -> bool:
    """
    Verifica si existe un usuario con el usuarioId proporcionado en la base de datos.

    Parámetros:
        - usuarioId (int): El ID del Usuario a verificar.
        - db: Conexión a la base de datos.

    Retorna:
        - True si el Usuario existe.
        - False si el Usuario no existe.
    
    Excepciones:
        - ServiceException(500, "Error al verificar la existencia del Usuario", extra={"usuarioId": usuarioId})
    """
    try:
        # Llamar a la función almacenada en la base de datos
        resultado = await realizarConexionBD(
            "verificarExistenciaUsuario",
            {"p_usuario_id": usuarioId},
            db,
            model=None,
            keep=True
        )

        # Acceder a los 'rows' del resultado
        rows = resultado.get("rows", [])
        
        # Verificar si hay datos en 'rows'
        if not rows:
            # No existe el usuario
            raise ServiceException(
                status_code=404,
                detail="No se encuentra el usuario solicitado",
                extra={"usuarioId": usuarioId}
            )
        # Obtener el valor de 'existe'
        existe = rows[0]['verificarexistenciausuario']

        # Retornar el resultado
        return existe
    
    except ServiceException as e:
        raise e

    except Exception as e:
        raise ServiceException(
            status_code=500,
            detail="Error al verificar la existencia del Usuario",
            extra={"error": str(e), "usuarioId": usuarioId}
        )
    

# Función para verificar la existencia de un usuario
async def verificarExistenciaUsuarioPorCuil(usuarioCuil: int, db) -> bool:
    """
    Verifica si existe un usuario con el cuil proporcionado del externo.

    Parámetros:
        - usuarioCuil (int): El cuil del Usuario a verificar.
        - db: Conexión a la base de datos.

    Retorna:
        - True si el Usuario existe.
        - False si el Usuario no existe.
    
    Excepciones:
        - ServiceException(500, "Error al verificar la existencia del Usuario", extra={"usuarioId": usuarioId})
    """
    try:
        # Llamar a la función almacenada en la base de datos
        resultado = await realizarConexionBD(
            "verificarExistenciaUsuarioPorCuil",
            {"p_usuario_cuil": usuarioCuil},
            db,
            model=None,
            keep=True
        )

        # Acceder a los 'rows' del resultado
        rows = resultado.get("rows", [])
        
        # Verificar si hay datos en 'rows'
        if not rows:
            # No existe el usuario
            raise ServiceException(
                status_code=404,
                detail="No se encuentra el usuario solicitado",
                extra={"usuarioCuil": usuarioCuil}
            )
        # Obtener el valor de 'existe'
        existe = rows[0]['verificarexistenciausuarioporcuil']

        # Retornar el resultado
        return existe
    
    except ServiceException as e:
        raise e

    except Exception as e:
        raise ServiceException(
            status_code=500,
            detail="Error al verificar la existencia del Usuario",
            extra={"error": str(e), "usuarioCuil": usuarioCuil}
        )