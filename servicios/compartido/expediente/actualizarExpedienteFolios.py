from db.databaseUtils import realizarConexionBD
from utils.error.errors import ErrorResponse, ServiceException

# Función que actualiza los folios actuales de un expediente
async def actualizarExpedienteFolios(expedienteId, expedienteFoliosActuales, db):
    """
    Parámetros:
        - expedienteId: int
        - expedienteFoliosActuales: int

    Retorna:
        - int: expedienteFoliosActuales

    Excepciones:
        - ServiceException(404, "No existe expediente con el id de expediente", extra={"expedienteId": expedienteId})
    """
    try:
        # Crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_expediente_id": expedienteId,
            "p_folios_actuales": expedienteFoliosActuales
        }
        # Obtener el tipo de expediente
        expedienteFoliosActualizadosList = await realizarConexionBD("actualizarFoliosExpediente", params, db, keep=True)

        expedienteFoliosActualizados = expedienteFoliosActualizadosList["rows"][0]

        return expedienteFoliosActualizados
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"No existe expediente con el id de expediente" in str(e):
            raise ServiceException(404, "No se encuentra el expediente solicitado a actualizar", extra={"expedienteId": expedienteId})
        elif f"El tipo de expediente se encuentra inactivo" in str(e):
            raise ServiceException(404, "El expediente solicitado a actualizar se encuentra inactivo", extra={"expedienteId": expedienteId})
        else:
            raise ServiceException(500, "Error al actualizar los folios del expediente", extra={"error": str(e), "expedienteId": expedienteId})