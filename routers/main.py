import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from routers.documento.documentoRouter import router as routerDocumento
from routers.expediente.expedienteRouter import router as routerExpediente
from routers.permiso.permisoRouter import router as routerPermiso
from routers.historialEstadoExpediente.historialEstadoExpedienteRouter import router as routerHistorialEstadoExpediente
from routers.movimiento.movimientoRouter import router as routerMovimiento
from routers.usuario.usuarioRouter import router as routerUsuario
from routers.tipoExpediente.tipoExpedienteRouter import router as routerTipoExpediente
from routers.estadoExpediente.estadoExpedienteRoute import router as routerEstadoExpediente
from routers.rol.rolRouter import router as routerRol
from routers.log.src.route.logRoute import router as routerLog
from routers.login.loginRouter import router as routerLogin
from utils.error.errors import validation_exception_handler, exception_handler, service_exception_handler, ServiceException
from pydantic_core import ValidationError

# Configuración del logger
logger = logging.getLogger("Expediente")
logger.setLevel(logging.DEBUG)

# Crear la instancia principal de la aplicación
app = FastAPI()

# Registrar los routers
app.include_router(routerDocumento)
app.include_router(routerExpediente)
app.include_router(routerHistorialEstadoExpediente, prefix="/historialEstadoExpediente")
app.include_router(routerMovimiento)
app.include_router(routerUsuario)
app.include_router(routerPermiso, prefix="/permiso")
app.include_router(routerTipoExpediente, prefix="/tipoExpediente")
app.include_router(routerEstadoExpediente, prefix="/estadoExpediente")
app.include_router(routerLog, prefix="/log")
app.include_router(routerRol, prefix="/rol")
app.include_router(routerLogin)

# Manejador global para errores 422
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(ServiceException, service_exception_handler)