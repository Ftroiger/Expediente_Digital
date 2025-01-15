from db.databaseUtils import realizarConexionBD
from utils.error.errors import ServiceException

# Función que actualiza los folios actuales de un expediente
async def actualizarExpedienteAreaActualidad(expedienteId, areaActualidadId, db):
    """
    Parámetros:
        - expedienteId: int
        - expedienteFoliosActuales: int

    Retorna:
        - int: expedienteFoliosActuales

    Excepciones:
        - ServiceException(404, "No existe expediente con el id de expediente", extra={"expedienteId": expedienteId})
        - ServiceException(404, "El expediente solicitado a actualizar se encuentra inactivo", extra={"expedienteId": expedienteId})
        - ServiceException(500, "Error al actualizar el área de actualidad del expediente", extra={"error": str(e)})
    """
    try:
        # Crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_expediente_id": expedienteId,
            "p_area_actualidad_id": areaActualidadId
        }
        # Obtener el tipo de expediente
        expedienteAreaActualidadActualizadaList = await realizarConexionBD("actualizarAreaActualidadExpediente", params, db, keep=True)

        expedienteAreaActualidadActualizada = expedienteAreaActualidadActualizadaList["rows"][0]

        return expedienteAreaActualidadActualizada
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if f"No existe expediente con el id de expediente" in str(e):
            raise ServiceException(404, "No se encuentra el expediente solicitado a actualizar", extra={"expedienteId": expedienteId})
        elif f"El expediente se encuentra inactivo" in str(e):
            raise ServiceException(404, "El expediente solicitado a actualizar se encuentra inactivo", extra={"expedienteId": expedienteId})
        else:
            raise ServiceException(500, "Error al actualizar el área de actualidad del expediente", extra={"error": str(e), "expedienteId": expedienteId})
