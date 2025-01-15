import logging
import os
from fastapi import Request, FastAPI, HTTPException
import httpx

from utils.error.errors import ServiceException

ID_APP = os.getenv("VEDI_ID_APP_TEST")
SECRET_APP = os.getenv("VEDI_SECRET_APP_TEST")
VEDI_API_BASE_URL = os.getenv("API_URL_BASE_TEST")

async def validateToken(token: str):
    # To complete when VEDI is ready
    datosUsuario = await obtenerDatosUsuarioVedi(token)
    if isinstance(datosUsuario, ServiceException):
        raise datosUsuario
    return datosUsuario


async def validarTokenSesion(sesionId: str):
    """Valida el token de sesión en el endpoint VEDI."""
    try:
        url = f"{VEDI_API_BASE_URL}v1/Usuario/ValidarTokenSesion"
        body = {
            "idAplicacion": ID_APP,
            "secret": SECRET_APP,
            "sesionId": sesionId
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=body)
            response.raise_for_status()
            responseData = response.json()
            if response.status_code in [400, 401, 403, 404, 500] or not responseData.get("ok"):
                raise ServiceException(
                    status_code=401,
                    detail=responseData.get("error")
                )
            return responseData.get("return").get("token"), responseData.get("return").get("refreshToken")
    
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ServiceException(
                status_code=e.response.status_code,
                detail="Token de acceso inválido o expirado. Por favor, inicie sesión nuevamente."
            )
        else:
            raise ServiceException(
                status_code=e.response.status_code,
                detail=f"Error al validar token de sesión: {e.response.text}"
            )


async def obtenerDatosUsuarioVedi(token: str):
    """Obtiene los datos del usuario desde el endpoint VEDI."""
    vediApiBaseUrl = "https://api.vedi.test.cordoba.gob.ar/WSVeDi_Bridge/"
    url = f"{vediApiBaseUrl}v3/Usuario/"
    headers = {
        "--token": token
    }
    

    async with httpx.AsyncClient() as client:
        try: 
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            responseData = response.json()

            if not responseData.get("ok"):
                raise ServiceException(
                    status_code=response.status_code,
                    detail=f"Error al obtener datos del usuario: {responseData.get('error')}"
                )
            return responseData.get("return")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ServiceException(
                    status_code=e.response.status_code,
                    detail="Token de acceso inválido o expirado. Por favor, inicie sesión nuevamente.",
                    extra={"error": e.response.text}
                )
            else:
                raise ServiceException(
                    status_code=e.response.status_code,
                    detail=f"Error al obtener datos del usuario: {e.response.text}"
                )
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail=f"Error inesperado: {str(e)}"
            )