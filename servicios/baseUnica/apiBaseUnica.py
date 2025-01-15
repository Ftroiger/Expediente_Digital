from utils.error.errors import ServiceException
import httpx
from datetime import datetime, timedelta, timezone
import os
from typing import List
from schemes.expedienteScheme import OrganigramaEntry
from pydantic import ValidationError

# Variables globales para almacenar el token y su expiración
baseUnicaToken = None
baseUnicaTokenExpiration = None

async def getBaseUnicaToken():
    global baseUnicaToken, baseUnicaTokenExpiration
    if baseUnicaToken is None or baseUnicaTokenExpiration <= datetime.now(timezone.utc):
        # Token expirado o no existe, obtener uno nuevo
        await loginBaseUnica()
    return baseUnicaToken

async def loginBaseUnica():
    """
    Realiza el login en Base Unica para obtener el token de autenticacion
    para luego poder hacer consultas y obtener el nombre de las areas para
    incluirlos en la carátula

    Retorna:
        "token_type": "string",
        "access_token": "string",
        "expiration": "string"
    """
    global baseUnicaToken, baseUnicaTokenExpiration

    # Obtener credenciales del entorno o configuración
    username = os.getenv("BASE_UNICA_USER")
    password = os.getenv("BASE_UNICA_PASS_PREPROD")

    # Validar que las credenciales estén presentes
    if not all([username, password]):
        raise ServiceException(status_code=500, detail="Faltan credenciales para autenticarse con Base Única")

    # Construir la URL
    baseUrl = "https://datos.stage.cordoba.gob.ar/api/base-unica/v3"  # Reemplaza con la URL real
    endpoint = "/login"  # Ajusta el endpoint según corresponda
    url = f"{baseUrl}{endpoint}"

    # Preparar los datos de la solicitud
    data = {
    "grant_type": "password",
    "username": username,
    "password": password,
    }

    # Definir los encabezados adecuados
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()

            respuesta = response.json()

            # Verificar que 'respuesta' es un diccionario y contiene los campos esperados
            if not isinstance(respuesta, dict):
                raise ServiceException(status_code=500, detail="La respuesta de Base Única no tiene el formato esperado")

            if "access_token" not in respuesta:
                raise ServiceException(status_code=500, detail="No se recibió un token en la respuesta de Base Única")

            # Almacenar el token y su tiempo de expiración
            baseUnicaToken = respuesta.get("access_token")
            expiration = respuesta.get("expiration")

            if expiration:
                baseUnicaTokenExpiration = datetime.fromisoformat(expiration)
            else:
                baseUnicaTokenExpiration = datetime.now(timezone.utc) + timedelta(hours=1)

            # Retornar el diccionario completo
            return respuesta

    except httpx.HTTPStatusError as exc:
        raise ServiceException(status_code=exc.response.status_code, detail=f"Error HTTP al comunicarse con Base Única: {exc.response.status_code}", extra={"response": exc.response.text})
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error inesperado al comunicarse con Base Única", extra={"error": str(e)})

async def getOrganigrama() -> List[OrganigramaEntry]:
    """
    Obtiene el organigrama (áreas) de la municipalidad desde la API de Base Única.

    Retorna:
        List[Dict]: Lista de áreas.
        Lanza ServiceException en caso de error.
    """
    # Obtener el token válido
    token = await getBaseUnicaToken()

    # Construir la URL
    baseUrl = "https://datos.stage.cordoba.gob.ar/api/base-unica/v3"
    endpoint = "/organigrama"
    url = f"{baseUrl}{endpoint}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            organigrama_data = response.json()

            # Procesar y validar la respuesta
            processed_organigrama = []
            for entry in organigrama_data:
                try:
                    processed_entry = OrganigramaEntry(**entry)  # Validar cada entrada
                    processed_organigrama.append(processed_entry.dict())  # Convertir a dict
                except ValidationError as e:
                    raise ServiceException(
                        status_code=422,
                        detail="Error de validación en la respuesta de organigrama",
                        extra={"entry": entry, "error": e.errors()}
                    )

            return processed_organigrama
    except ServiceException as e:
        raise e
    except httpx.HTTPStatusError as exc:
        raise ServiceException(status_code=exc.response.status_code, detail=f"Error HTTP al comunicarse con Base Única: {exc.response.status_code}", extra={"response": exc.response.text})
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error inesperado al comunicarse con Base Única", extra={"error": str(e)})
    
async def getDependenciaById(idDependencia: int) -> dict:
    """
    Obtiene una dependencia (área) de la municipalidad por su ID desde la API de Base Única.

    Parámetros:
        id_dependencia (int): ID de la dependencia a buscar.

    Retorna:
        dict: Información de la dependencia obtenida.
    """
    # Obtener el token válido
    token = await getBaseUnicaToken()

    # Construir la URL
    baseUrl = "https://datos.stage.cordoba.gob.ar/api/base-unica/v3"
    endpoint = f"/dependencias"
    url = f"{baseUrl}{endpoint}"

    # Establecer los encabezados y parámetros
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "p_id_dependencia": idDependencia
    }

    try:
        async with httpx.AsyncClient() as client:
            # Realizar la solicitud GET con los parámetros y encabezados
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()

            dependenciaData = response.json()
            return dependenciaData
        
    except ServiceException as e:
        raise e
    except httpx.HTTPStatusError as exc:
        raise ServiceException(
            status_code=exc.response.status_code, 
            detail=f"Error HTTP al comunicarse con Base Única: {exc.response.status_code}", 
            extra={"response": exc.response.text}
        )
    except Exception as e:
        raise ServiceException(
            status_code=500, 
            detail="Error inesperado al comunicarse con Base Única", 
            extra={"error": str(e)}
        )
