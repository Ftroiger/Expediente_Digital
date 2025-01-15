from utils.error.errors import ServiceException

def obtenerAuditoriaHeader(request):
    """
    Función que obtiene los datos de auditoria del header de la petición.
    :param request: Petición HTTP.
    :return: Diccionario con los datos de auditoria.
    """
    try:
        datos = {
            'host': request.headers.get('Host'),
            'userAgent': request.headers.get('User-Agent'),
            'ipAddress': request.client.host,
        }
        return datos

    except Exception as e:
        raise ServiceException(500, "Error al obtener los datos del header", extra={"message": str(e)})
