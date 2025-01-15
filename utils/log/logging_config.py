import logging
import uuid
from logging.handlers import TimedRotatingFileHandler

# Configuración del logger principal
logger = logging.getLogger("Expediente")

# Filtro personalizado para agregar un ID único a cada registro de log
class UniqueIDFilter(logging.Filter):
    def filter(self, record):
        record.unique_id = uuid.uuid4()  # Genera un ID único para cada registro
        return True

# Función auxiliar para configurar un handler para archivos
def create_file_handler(log_file):
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, encoding='utf-8')
    handler.suffix = "%Y%m%d"
    handler.addFilter(UniqueIDFilter())
    formatter = logging.Formatter(
        'ID: %(unique_id)s /-/ Fecha: %(asctime)s /-/ Servicio: %(name)s /-/ Nivel: %(levelname)s /-/ '
        'Archivo: %(module)s /-/ Clase: %(funcName)s /-/ Descripcion: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    return handler

# Crear y agregar handlers al logger principal
file_handler = create_file_handler("expediente.log")
logger.addHandler(file_handler)

# Función para setear un logger
def loggerSetup(nombre: str, archivoLog: str, level=logging.DEBUG):
    logger = logging.getLogger(nombre)
    logger.setLevel(level)
    logger.propagate = False

    # Verificar si el logger ya tiene handlers
    if not logger.handlers:
        logger.addHandler(create_file_handler(archivoLog))
    return logger

# Logger gateway y expediente
loggerExpediente = loggerSetup("Expediente", "expediente.log")
loggerExpediente = loggerSetup("Gateway", "expediente.log")
