import httpx
from datetime import datetime, timedelta, timezone
import os
import base64
from utils.error.errors import ServiceException

# Variables globales para almacenar el token y su expiración
siradToken = None
siradTokenExpiration = None

async def loginSirad():
    """
    Realiza el login en SIRAD y obtiene un token de autenticación.

    Retorna:
        str: Token de autenticación si el login es exitoso.
        ErrorResponse: En caso de error.
    """
    global siradToken, siradTokenExpiration

    # Obtener credenciales del entorno o configuración
    username = os.getenv("SIRAD_USERNAME")
    password = os.getenv("SIRAD_PASSWORD")
    codigoEntidad = os.getenv("SIRAD_CODIGO_ENTIDAD")

    # Validar que las credenciales estén presentes
    if not all([username, password, codigoEntidad]):
        raise ServiceException(status_code=500, detail="Faltan credenciales para autenticarse con SIRAD")

    # Construir la URL
    baseUrl = "https://srv-dev04.cordoba.local/SiradApi"
    endpoint = "/api/login/LoginUsuario"
    url = f"{baseUrl}{endpoint}"

    # Preparar los datos de la solicitud
    data = {
        "Username": username,
        "Password": password,
        "CodigoEntidad": codigoEntidad
    }

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, json=data)
            response.raise_for_status()

            # Intentar decodificar la respuesta JSON
            try:
                respuesta = response.json()
            except ValueError as e:
                raise ServiceException(status_code=500, detail="La respuesta de SIRAD no es un JSON válido", extra={"error": str(e)})

            # Verificar que 'respuesta' es un diccionario
            if not isinstance(respuesta, dict):
                raise ServiceException(status_code=500, detail="La respuesta de SIRAD no tiene el formato esperado")

            if "Error" in respuesta and respuesta["Error"]:
                raise ServiceException(status_code=500, detail=f"Error en el login de SIRAD: {respuesta['Error']}", extra={"response": respuesta})

            token = respuesta.get("Token")

            if not token:
                raise ServiceException(status_code=500, detail="No se recibió un token en la respuesta de SIRAD")

            # Almacenar el token y su tiempo de expiración
            siradToken = token
            siradTokenExpiration = datetime.now(timezone.utc) + timedelta(hours=1)

            return token

    except httpx.HTTPStatusError as exc:
        raise ServiceException(status_code=exc.response.status_code, detail=f"Error HTTP al comunicarse con SIRAD: {exc.response.status_code}", extra={"response": exc.response.text})

    except Exception as e:
        raise ServiceException(status_code=500, detail="Error inesperado al comunicarse con SIRAD", extra={"error": f"Es posible que sea un problema de conexión VPN/Proxy. {str(e)}"})

async def crearDocumentoSirad(data):
    """
    Envía una solicitud POST al API de SIRAD para crear un documento que le pasamos tipoExpediente que es un expediente.

    Parámetros:
        data: dict -> Datos validados que se enviarán a SIRAD.

    Retorna:
        dict -> Respuesta de SIRAD.
    """
    global siradToken, siradTokenExpiration

    # Verificar si el token es válido o necesita renovarse
    if not siradToken or datetime.now(timezone.utc) >= siradTokenExpiration:
        tokenResponse = await loginSirad()

        siradToken = tokenResponse

    # Base URL para el entorno de pruebas de SIRAD
    baseUrl = "https://srv-dev04.cordoba.local/SiradApi"
    endpoint = "/api/documentos/CrearDocumento"
    url = f"{baseUrl}{endpoint}"

    # Incluir el código de entidad y el token en los encabezados
    codigoEntidad = os.getenv("SIRAD_CODIGO_ENTIDAD")
    headers = {
        "Content-Type": "application/json",
        "Codigo-Entidad": codigoEntidad,
        "Authorization": f"Bearer {siradToken}"
    }

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP 4xx y 5xx

            # Suponiendo que la respuesta es JSON
            respuesta = response.json()

            # Manejar posibles errores en la respuesta
            if respuesta.get("Error"):
                raise ServiceException(status_code=500, detail=f"Error en la respuesta de SIRAD: {respuesta['Error']}", extra={"response": respuesta})


            # Verificar que los campos necesarios están presentes
            if not all(k in respuesta for k in ("IdentificadorUnico", "Mascara", "Id")):
                raise ServiceException(status_code=500, detail="La respuesta de SIRAD no contiene los campos esperados")

            
            # Modificar la Mascara de SIRAD para sacarle el "/"
            respuesta["Mascara"] = respuesta["Mascara"].replace("/", "-")
            respuesta["Mascara"] = respuesta["Mascara"].replace(" ", "-")

            return respuesta

    except httpx.HTTPStatusError as exc:
        raise ServiceException(status_code=exc.response.status_code, detail=f"Error HTTP al comunicarse con SIRAD: {exc.response.status_code}", extra={"response": exc.response.text})

    except Exception as e:
        raise ServiceException(status_code=500, detail="Error inesperado al comunicarse con SIRAD", extra={"error": str(e)})

async def consultarTemas():
    """
    Consulta la lista de temas desde el API de SIRAD.

    Retorna:
        list: Lista de temas si la consulta es exitosa.
        ErrorResponse: En caso de error.
    """
    global siradToken, siradTokenExpiration

    # Verificar si el token es válido o necesita renovarse
    if not siradToken or datetime.now(timezone.utc) >= siradTokenExpiration:
        token_response = await loginSirad()

        siradToken = token_response

    # Base URL para el entorno de SIRAD
    baseUrl = "https://srv-dev04.cordoba.local/SiradApi"
    endpoint = "/api/documentos/ConsultarTemas"
    url = f"{baseUrl}{endpoint}"

    # Incluir el código de entidad y el token en los encabezados
    codigoEntidad = os.getenv("SIRAD_CODIGO_ENTIDAD")
    headers = {
        "Content-Type": "application/json",
        "Codigo-Entidad": codigoEntidad,
        "Authorization": f"Bearer {siradToken}"
    }

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            # Intentar decodificar la respuesta JSON
            try:
                respuesta = response.json()
            except ValueError as e:
                raise ServiceException(status_code=500, detail="La respuesta de SIRAD no es un JSON válido", extra={"error": str(e)})


            # Verificar que 'respuesta' es un diccionario
            if not isinstance(respuesta, dict):
                raise ServiceException(status_code=500, detail="La respuesta de SIRAD no tiene el formato esperado", extra={"response": respuesta})


            # Manejar posibles errores en la respuesta
            if "Error" in respuesta and respuesta["Error"]:
                raise ServiceException(status_code=500, detail=f"Error en la respuesta de SIRAD: {respuesta['Error']}", extra={"response": respuesta})


            # Verificar que 'ListaTemas' está presente
            if "listaTemas" not in respuesta:
                raise ServiceException(status_code=500, detail="La respuesta de SIRAD no contiene la lista de temas", extra={"response": respuesta})

            return respuesta["listaTemas"]

    except httpx.HTTPStatusError as exc:
        raise ServiceException(status_code=exc.response.status_code, detail=f"Error HTTP al comunicarse con SIRAD: {exc.response.status_code}", extra={"response": exc.response.text})

    except Exception as e:
        raise ServiceException(status_code=500, detail="Error inesperado al comunicarse con SIRAD", extra={"error": str(e)})

async def generarCaratulaSirad(idExpedienteSirad):
    """
    Sends a GET request to SIRAD to generate the carátula for the given expediente ID.

    Parameters:
        idExpedienteSirad: int -> ID of the expediente in SIRAD.

    Returns:
        dict -> Response from SIRAD.
    """
    global siradToken, siradTokenExpiration

    if not siradToken or datetime.now(timezone.utc) >= siradTokenExpiration:
        siradToken = await loginSirad()

    baseUrl = "https://srv-dev04.cordoba.local/SiradApi"
    endpoint = "/api/impresion/GenerarCaratula"
    url = f"{baseUrl}{endpoint}"

    codigoEntidad = os.getenv("SIRAD_CODIGO_ENTIDAD")
    headers = {
        "Content-Type": "application/json",
        "Codigo-Entidad": codigoEntidad,
        "Authorization": f"Bearer {siradToken}"
    }

    params = {"id": idExpedienteSirad}

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors

            response_data = response.json()
            # Process the response
            error = response_data.get("Error", "")
            document_bytes_base64 = response_data.get("DocumentBytes", "")
            document_name = response_data.get("DocumentName", "")
            document_extension = response_data.get("DocumentExtension", "")
            document_mime_type = response_data.get("DocumentMimeType", "")

            # Decode the document bytes from base64
            document_bytes = base64.b64decode(document_bytes_base64) if document_bytes_base64 else None

            return {
                "Error": error,
                "DocumentBytes": document_bytes,
                "DocumentName": document_name,
                "DocumentExtension": document_extension,
                "DocumentMimeType": document_mime_type
            }
    except httpx.HTTPStatusError as exc:
        error_message = f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}"
        return {
            "Error": error_message,
            "DocumentBytes": None,
            "DocumentName": "",
            "DocumentExtension": "",
            "DocumentMimeType": ""
        }
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return {
            "Error": error_message,
            "DocumentBytes": None,
            "DocumentName": "",
            "DocumentExtension": "",
            "DocumentMimeType": ""
        }


# async def generarCaratulaSirad(idExpedienteSirad):
#     """
#     Envia los datos de la caratula a SIRAD para que este cree la caratula en su sistema

#     parámetros: 
#         idExpedienteSirad: int -> id del expediente en sirad

#     Retorna:
#         dict -> Respuesta de SIRAD.
#     """
#     global siradToken, siradTokenExpiration

#     if not siradToken or datetime.now(timezone.utc) >= siradTokenExpiration:
#         siradToken = await loginSirad()

#     baseUrl = "https://srv-dev04.cordoba.local/SiradApi"
#     endpoint = "/api/impresion/GenerarCaratula"
#     url = f"{baseUrl}{endpoint}"

#     codigoEntidad = os.getenv("SIRAD_CODIGO_ENTIDAD")
#     headers = {
#         "Content-Type": "application/json",
#         "Codigo-Entidad": codigoEntidad,
#         "Authorization": f"Bearer {siradToken}"
#     }

#     try:
#         # Disable SSL verification for development purposes
#         connector = aiohttp.TCPConnector(ssl=False)
#         async with aiohttp.ClientSession(connector=connector) as session:
#             params = {"id": idExpedienteSirad}
#             async with session.get(url, headers=headers, params=params) as response:
#                 if response.status == 200:
#                     response_data = await response.json()
#                     # Procesar la respuesta
#                     error = response_data.get("Error", "")
#                     document_bytes_base64 = response_data.get("DocumentBytes", "")
#                     document_name = response_data.get("DocumentName", "")
#                     document_extension = response_data.get("DocumentExtension", "")
#                     document_mime_type = response_data.get("DocumentMimeType", "")

#                     # Decodificar los bytes del documento desde base64
#                     document_bytes = base64.b64decode(document_bytes_base64) if document_bytes_base64 else None

#                     return {
#                         "Error": "",
#                         "DocumentBytes": document_bytes,
#                         "DocumentName": document_name,
#                         "DocumentExtension": document_extension,
#                         "DocumentMimeType": document_mime_type
#                     }

#                     # # Guardar el documento en la carpeta Downloads
#                     # try:
#                     #     file_path = guardarCaratula(caratula_data)
#                     #     return {
#                     #         "Error": error,
#                     #         "FilePath": file_path,
#                     #         "DocumentName": document_name,
#                     #         "DocumentExtension": document_extension,
#                     #         "DocumentMimeType": document_mime_type
#                     #     }
#                     # except Exception as save_error:
#                     #     return {
#                     #         "Error": f"Error al guardar la carátula: {str(save_error)}",
#                     #         "DocumentBytes": None,
#                     #         "DocumentName": "",
#                     #         "DocumentExtension": "",
#                     #         "DocumentMimeType": ""
#                     #     }
#                 else:
#                     # Manejar errores HTTP
#                     error_text = await response.text()
#                     return {
#                         "Error": f"Error HTTP {response.status}: {error_text}",
#                         "DocumentBytes": None,
#                         "DocumentName": "",
#                         "DocumentExtension": "",
#                         "DocumentMimeType": ""
#                     }
#     except Exception as e:
#         # Manejar excepciones
#         return {
#             "Error": str(e),
#             "DocumentBytes": None,
#             "DocumentName": "",
#             "DocumentExtension": "",
#             "DocumentMimeType": ""
#         }

# #Función temporaria que usamos para verificar que funciones la request de crear caratula a SIRAD
# def guardarCaratula(caratula_data):
#     """
#     Decodifica y guarda la carátula como un archivo PDF en la carpeta 'Downloads' del usuario.

#     parámetros:
#         caratula_data: dict -> Diccionario con los datos de la carátula (DocumentBytes, DocumentName, etc.)

#     retorna:
#         str -> Ruta completa del archivo guardado.
#     """
#     # Obtener la carpeta 'Downloads' del usuario
#     downloads_dir = Path.home() / "Downloads"
#     downloads_dir.mkdir(exist_ok=True)  # Asegurarse de que exista

#     # Extraer datos del documento
#     document_bytes = caratula_data.get("DocumentBytes", None)
#     document_name = caratula_data.get("DocumentName", "Caratula")  # Nombre por defecto
#     document_extension = caratula_data.get("DocumentExtension", "pdf")  # Extensión por defecto

#     if not document_bytes:
#         raise Exception("No se recibieron bytes del documento para guardar.")

#     # Nombre del archivo completo
#     file_path = downloads_dir / f"{document_name}.{document_extension}"

#     try:
#         # Guardar el archivo como PDF
#         with open(file_path, "wb") as file:
#             file.write(document_bytes)

#         print(f"Carátula guardada en: {file_path}")
#         return str(file_path)
#     except Exception as e:
#         raise Exception(f"Error al guardar la carátula: {e}")
