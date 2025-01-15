import datetime
import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from utils.log.logging_config import loggerExpediente

# Configuración del logger
logger = logging.getLogger("Expediente")
logger.setLevel(logging.DEBUG)

# --- Custom response de Error ---
class ErrorResponse(JSONResponse):
    def __init__(self, status_code: int, detail: str, extra: dict = None, origin: str = None, success: bool = False):
        content = {
            "status_code": status_code,
            "detail": detail,
            "success": success,
            "timestamp": datetime.datetime.now().isoformat()
        }
        if extra:
            content["extra"] = extra

        self._content_data = content

        super().__init__(status_code=status_code, content=content)

        # Agregar CORS headers si `origin` existe
        if origin:
            self.headers["Access-Control-Allow-Origin"] = origin
            self.headers["Access-Control-Allow-Credentials"] = "true"

    # Método para obtener el contenido de manera segura
    def get_content(self):
        return self._content_data
    
    # Método str()
    def __str__(self):
        return f"ErrorResponse: {self._content_data}"
    


# ---- HANDLERS ----

# Clase para manejar excepciones en los servicios
class ServiceException(Exception):
    def __init__(self, status_code: int, detail: str, extra: dict = None):
        self.status_code = status_code
        self.detail = detail
        self.extra = extra

    def to_response(self):
        return ErrorResponse(status_code=self.status_code, detail=self.detail, extra=self.extra)
    
    # Función a str
    def __str__(self):
        return f"ServiceException: {self.status_code} - {self.detail} - {self.extra}"
    

# Manejador global para ServiceExceptions
async def service_exception_handler(request: Request, exc: ServiceException):
    # Registrar el error en el log
    logger.error(f"Error en la solicitud a {request.url}: {exc}")
    # Devolver en ErrorResponse
    return exc.to_response()


# Manejador global para errores de validación 422
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Registrar el error en el log
    try:
        logger.error(f"Error de validación en la solicitud a {request.url}: {exc.errors()}")
        first_error = exc.errors()[0] if exc.errors() else None
        error_type_translations = {
            "missing": "es requerido.",
            "string_type": "debe ser una cadena de texto.",
            "int_parsing": "debe ser un número entero.",
            "bool_parsing": "debe ser un valor booleano.",
            "too_short": "tiene una cantidad inferior a {min_length}.",
            "uuid_parsing": "debe ser un uuid válido.",
            "enum": "debe ser uno de los valores permitidos.",
            "greater_than": "debe ser mayor que {gt}.",
            "greater_than_equal": "debe ser mayor o igual que {ge}.",
            "literal_error": "debe ser uno de los siguientes valores {expected}.",
            "json_invalid": "JSON invalido.",
            "value_error": "{error}.",   
        }
        if first_error:
            loc = first_error["loc"][-1].replace("_", " ")
            readable_error = error_type_translations.get(
                first_error["type"], first_error["msg"]
            )
            if first_error.get("ctx"):
                ctx_value = {**first_error["ctx"]}
                if first_error["type"] == "literal_error" and "expected" in ctx_value:
                    ctx_value["expected"] = ctx_value["expected"].replace(" or ", ", ")
                readable_error = readable_error.format(
                    **{
                        k: v
                        for k, v in ctx_value.items()
                        if k in ["gt", "min_length", "error","ge","expected"]
                    }
                )
            error_message = f"{loc} {readable_error}"

        else:
            error_message = "Error desconocido"

        return ErrorResponse(status_code=422, detail="Error de validación en los datos enviados.", extra={"error": error_message})

    except Exception as e:
        return ErrorResponse(status_code=500, detail="Error al manejar la excepción de validación.", extra={"error": str(e)})
    

# Manejador globar errores 500
async def exception_handler(request: Request, exc: Exception):
    # Registrar el error en el log
    logger.error(f"Error en la solicitud a {request.url}: {exc}")
    return ErrorResponse(status_code=500, detail="Error interno en el servidor", extra={"error": str(exc)})
