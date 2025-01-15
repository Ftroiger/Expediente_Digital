from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
import httpx
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic_core import ValidationError

from schemes.usuarioScheme import UsuarioCreate
from servicios.compartido.auditoria.completarAuditoria import completarAuditoriaRolXUsuarioGateWay, completarAuditoriaUsuarioGateway
from servicios.compartido.obtenerDatosAuditoria import obtenerAuditoriaHeader
from servicios.compartido.rol.obtenerRoles import obtenerRolPorNombre
from servicios.compartido.usuario.insertarUsuarioBdd import insertarUsuario
from .auth import validarTokenSesion, validateToken
from utils.error.errors import ErrorResponse, ServiceException, exception_handler, service_exception_handler, validation_exception_handler
from starlette.middleware.cors import CORSMiddleware
from servicios.compartido.usuario.obtenerUsuario import verificarExistenciaUsuarioAplicacion, verificarExistenciaUsuarioPorCuil
from servicios.compartido.usuario.obtenerUsuario import obtenerUsuarioPorCuil
from db.database import get_db
import logging

# Configurar el logging
logger = logging.getLogger("Gateway")
logger.setLevel(logging.DEBUG)  # Ajusta el nivel según tus necesidades

# Agarrar env
load_dotenv()

# FastAPI app para el gateway
app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

URLS_MICROSERVICIOS = {
    "documento": os.getenv("MICROSERVICIO_DOCUMENTO"),
    "permiso": os.getenv("MICROSERVICIO_PERMISO"),
    "usuario": os.getenv("MICROSERVICIO_USUARIO"),
    "tipoNorma": os.getenv("MICROSERVICIO_TIPO_NORMA"),
    "norma": os.getenv("MICROSERVICIO_NORMA"),
    "expediente": os.getenv("MICROSERVICIO_EXPEDIENTE"),
    "historialEstadoExpediente": os.getenv("MICROSERVICIO_HISTORIAL_ESTADO_EXPEDIENTE"),
    "expedienteXNorma": os.getenv("MICROSERVICIO_EXPEDIENTE_X_NORMA"),
    "movimiento": os.getenv("MICROSERVICIO_MOVIMIENTO"),
    "tipoExpediente": os.getenv("MICROSERVICIO_TIPO_EXPEDIENTE"),
    "estadoExpediente": os.getenv("MICROSERVICIO_ESTADO_EXPEDIENTE"),
    "documentoXMovimiento": os.getenv("MICROSERVICIO_DOCUMENTO_X_MOVIMIENTO"),
    "log": os.getenv("MICROSERVICIO_LOG"),
    "rol": os.getenv("MICROSERVICIO_ROL"),
    "login" : os.getenv("MICROSERVICIO_LOGIN"),
    "permiso": os.getenv("MICROSERVICIO_PERMISO"),
}


# Gateway middleware
@app.middleware("http")
async def proxy_request(request: Request, call_next):
    try:
        # Manejar preflight options request
        if request.method == "OPTIONS":
            return JSONResponse(status_code=200, headers={
                "Access-Control-Allow-Origin": request.headers.get("origin"),
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
            }, content={}, success=True)
        
        # Extraer origin del request
        origin = request.headers.get("origin")

        # ---- AUTENTICACION ----
        # Agarrar instancia de BD
        db = next(get_db())
        
        # Si es un sistema vertical, tiene que proveer su propio usuarioAplicacionId y su apiKey por headers
        usuarioAplicacionId = request.headers.get("X-Usuario-Id")
        apiKey = request.headers.get("X-Api-Key")

        # Puede ser que sea un Usuario, en cuyo caso tiene que proveer un token de vedi
        tokenVedi = request.headers.get("--token")
    

        # Caso 1: Si se proporcionan usuarioAplicacionId y apiKey
        if usuarioAplicacionId and apiKey:
            logger.debug(f"Autenticando usuarioAplicacionId: {usuarioAplicacionId}, apiKey: {apiKey}")
            # Verificar la existencia del usuarioAplicacion
            if not await verificarExistenciaUsuarioAplicacion(int (usuarioAplicacionId), str (apiKey), db):
                db.rollback()
                error = ErrorResponse(
                    status_code=401,
                    detail="Sistema vertical no autorizado. Credenciales inválidas",
                    origin=origin,
                    success=False,
                    extra={"usuarioAplicacionId": usuarioAplicacionId}
                )
                logger.error(f"Error en la autenticación: " + str(error))
                return error
            
            usuarioVedi = None



            # En el caso de pasar el token de vedi directamente, validar y extraer el cuil
            if tokenVedi:
                usuarioVedi = await validateToken(tokenVedi)
            # DESPUES SACAR ---- ESTO ES PARA NO TENER QUE PASAR TOKEN SIEMPRE
            else:
                usuarioVedi = {"cuil": "20333333333", "nombre": "Usuario", "apellido": "Vedi"}

            
            
            # Si no se extrae el usuario
            if not usuarioVedi:
                db.rollback()
                error = ErrorResponse(
                    status_code=401,
                    detail="Token de VEDI inválido.",
                    origin=origin,
                    success=False,
                    extra={"usuarioAplicacionId": usuarioAplicacionId}
                )
                logger.error(f"Error en la autenticación: " + str(error))
                return error

            # Al recibir los detalles de usuario de Vedi, verificar si existe en la base de datos
            usuarioExiste = await verificarExistenciaUsuarioPorCuil(usuarioVedi.get("cuil"), db)

            # Si no existe el usuario, crealo
            if not usuarioExiste:
                # Agarra el rol id por nombre "Usuario Fisico"
                rolUsuarioFisico = await obtenerRolPorNombre("Usuario Fisico", db)

                usuarioCreate = UsuarioCreate(
                    nombreUsuario=usuarioVedi.get("nombre") + " " + usuarioVedi.get("apellido"),
                    cuilUsuario=usuarioVedi.get("cuil"),        
                )
                # Insertar el usuario en la base de datos
                datosAuditoria = obtenerAuditoriaHeader(request)
                usuario = await insertarUsuario(1, usuarioCreate, rolUsuarioFisico.rolId, db)
                await completarAuditoriaUsuarioGateway(
                    usuario.usuarioId,
                    usuarioAplicacionId,
                    datosAuditoria, 
                    db
                )
                await completarAuditoriaRolXUsuarioGateWay(
                    usuario.usuarioId,
                    usuarioAplicacionId,
                    datosAuditoria,
                    db
                )

            usuarioResponsable = await obtenerUsuarioPorCuil(usuarioVedi.get("cuil"), db)
            # Guardar el usuarioId del responsable en el request
            request.state.usuarioId = str(usuarioAplicacionId)
            request.state.usuarioResponsableId = str(usuarioResponsable.usuarioId)
            # Continuar si es válido
            db.commit()

        # Caso 2: Si solo se proporciona el token de VEDI
        elif tokenVedi:
            try:
                usuarioVedi = await validateToken(tokenVedi)

                # Al recibir los detalles de usuario de Vedi, verificar si existe en la base de datos
                usuarioExiste = await verificarExistenciaUsuarioPorCuil(usuarioVedi.get("cuil"), db)

                # Si no existe el usuario, crealo
                if not usuarioExiste:
                    # Agarra el rol id por nombre "Usuario Fisico"
                    rolUsuarioFisico = await obtenerRolPorNombre("Usuario Fisico", db)

                    usuarioCreate = UsuarioCreate(
                        nombreUsuario=usuarioVedi.get("nombre") + " " + usuarioVedi.get("apellido"),
                        cuilUsuario=usuarioVedi.get("cuil"),        
                    )
                    # Insertar el usuario en la base de datos
                    await insertarUsuario(1, usuarioCreate, rolUsuarioFisico.rolId, db)
    
                # Se obtiene el usuario responsable
                usuario = await obtenerUsuarioPorCuil(usuarioVedi.get("cuil"), db)

                # Si se encuentra, guardar el usuarioId en los headers
                request.state.usuarioId = str(usuario.usuarioId)
                request.state.usuarioResponsableId = str(usuario.usuarioId)
                db.commit()
            
            except ServiceException as e:
                db.rollback()
                error = ErrorResponse(
                    status_code=401,
                    detail="Token de VEDI inválido.",
                    origin=origin,
                    success=False,
                    extra={"tokenVedi": tokenVedi, "error": e.detail}
                )
                logger.error(f"Error en la autenticación: " + str(error))
                return error
            
            except Exception as e:
                db.rollback()
                error = ErrorResponse(
                    status_code=401,
                    detail="Token de VEDI inválido.",
                    origin=origin,
                    success=False,
                    extra={"tokenVedi": tokenVedi, "error": str(e)}
                )
                logger.error(f"Error en la autenticación: " + str(error))
                return error

        # Caso 3: Si no se proporciona ninguna credencial
        else:
            db.rollback()
            error = ErrorResponse(
                status_code=401,
                detail="No se ha proporcionado credenciales.",
                origin=origin,
                success=False
            )
            logger.error(f"Error en la autenticación: " + str(error))
            # Redirigir a VEDI y comenzar de nuevo - REEMPLAZAR CON ESO
            return error
        

        db.close()

        # Extrae la primera parte de la URL para determinar el microservicio
        # de http://localhost:8000/usuario/1 request.url.path = /usuario/1
        path = request.url.path.lstrip("/") # usuario/1
        microservicio = path.split("/")[0] # usuario
        microservicio_url = URLS_MICROSERVICIOS.get(microservicio) 
        
        # Si el microservicio no existe, regresa un error
        if not microservicio_url:
            error = ErrorResponse(status_code=404, detail=f"Microservicio {microservicio} no encontrado", success=False, origin=origin)
            logger.error(f"Error en el Gateway: " + str(error))
            return error

        # Construye URL del microservicio
        proxy_url = f"{microservicio_url}/{path}"

        # Redirigir solicitud al microservicio
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # Agregar objeto de usuario al header
                headers = dict(request.headers)
                if request.state.usuarioId and request.state.usuarioResponsableId:
                    headers["X-Usuario-Id"] = str(request.state.usuarioId)
                    headers["X-Usuario-Responsable-Id"] = str(request.state.usuarioResponsableId)

                # Enviar solicitud al microservicio y obtener respuesta
                response = await client.request(
                    method=request.method,
                    url=proxy_url,
                    headers=headers,
                    data=await request.body(),
                    params=request.query_params,
                    follow_redirects=False
                )

                # Manejar si el resultado fue otro redirect
                if response.status_code in [301, 302, 303, 307, 308]:
                    # Manejar redirección si es el mismo dominio
                    if response.headers.get("location") == str(request.url):
                        return ErrorResponse(
                            status_code=500,
                            detail="Redirect loop detected",
                            extra={"message": "Redirecting to the same URL"},
                            success=False,
                            origin=origin
                        )
                    return RedirectResponse(url=response.headers["location"])


                # Armar la respuesta
                custom_response = JSONResponse(
                    status_code= response.status_code,
                    content=(
                        response.json()
                        if response.headers.get("content-type") == "application/json"
                        else {
                            "detail": "Respuesta no es JSON",
                            "body": response.text,
                        }
                    ),
                )

                # Agregar CORS headers
                if(origin):
                    custom_response.headers["Access-Control-Allow-Origin"] = origin
                # Cookies
                custom_response.headers["Access-Control-Allow-Credentials"] = "true"

                return custom_response
            
            except ServiceException as e:
                db.rollback()
                error = ErrorResponse(status_code=e.status_code, detail=e.detail, extra=e.extra, success=False, origin=origin)
                logger.error(f"Error en el Gateway: " + str(error))
                return error

            except httpx.RequestError as exc:
                db.rollback()
                error = ErrorResponse(status_code=502, detail=f"Error al comunicarse con {microservicio}", extra={"message": str(exc)}, success=False, origin=origin)
                logger.error(f"Error en el Gateway: " + str(error))
                return error
            except Exception as e:
                db.rollback()
                error = ErrorResponse(status_code=500, detail="Error interno", extra={"message": str(e)}, success=False, origin=origin)
                logger.error(f"Error en el Gateway: " + str(error))
                return error
    
    except ServiceException as e:
        error = ErrorResponse(status_code=e.status_code, detail=e.detail, extra=e.extra, success=False, origin=origin)
        logger.error(f"Error en el Gateway: " + str(error))
        return error

    except Exception as e:
        error = ErrorResponse(status_code=500, detail="Error interno", extra={"message": str(e)}, success=False, origin=origin)
        logger.error(f"Error en el Gateway: " + str(error))
        return error
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)