from db.databaseUtils import realizarConexionBD
from db.models.tipoExpediente import TipoExpediente
from utils.error.errors import ServiceException

# Función que obtiene el id del expediente tipo expediente
async def obtenerExpedienteTipoExpediente(db) -> TipoExpediente:
    try:
        # Crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_nombreTipoExpediente": "Expediente"
        }
        # Obtener el tipo de expediente
        tipoExpedienteList = await realizarConexionBD("obtenerTipoExpedientePorNombre", params, db, model=TipoExpediente, keep=True)
        tipoExpediente = tipoExpedienteList["rows"][0]
        
        return tipoExpediente
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"No existe ese tipo de expediente" in str(e):
            raise ServiceException(404, "No existe el tipo de expediente solicitado", extra={"tipoExpediente": "Expediente"})
        elif f"El tipo de expediente se encuentra inactivo" in str(e):
            raise ServiceException(404, "El tipo de expediente se encuentra inactivo", extra={"tipoExpediente": "Expediente"})
        else:
            raise ServiceException(500, "Error al obtener el tipo de expediente", extra={"error": str(e)})
