import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

from utils.error.errors import ServiceException

#Variables globales para almacenar token y refresh token

VEDI_TOKEN = None
VEDI_REFRESH_TOKEN = None

# Load environment variables
load_dotenv()

ID_APP = os.getenv("VEDI_ID_APP_TEST")
SECRET_APP = os.getenv("VEDI_SECRET_APP_TEST")
VEDI_API_BASE_URL = os.getenv("API_URL_BASE_TEST")

app = FastAPI()

class LoginRequest(BaseModel):
    cuil: str
    password: str

class TokenManager:
    def __init__(self):
        self.token = None
        self.refresh_token = None

    async def validar_Token_Sesion(self, sesion_id):
        url = f"{VEDI_API_BASE_URL}v1/Usuario/ValidarTokenSesion"
        body = {
            "idAplicacion": ID_APP,
            "secret": SECRET_APP,
            "sesionId": sesion_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=body)
            response.raise_for_status()
            response_data = response.json()
            if response.status_code in [400, 401, 403, 404, 500] or not response_data.get("ok"):
                raise ServiceException(status_code=401, detail=response_data.get("error"))
            self.token = response_data.get("return").get("token")
            self.refresh_token = response_data.get("return").get("refreshToken")

    
    async def obtener_token_valido(self, sesion_id):
        if not self.token:
            await self.validar_Token_Sesion(sesion_id)
        return self.token

    async def obtener_Datos_Usuario_Vedi(self, token: str):
        """Obtiene los datos del usuario desde el endpoint VEDI."""
        VEDI_API_BASE_URL = "https://api.vedi.test.cordoba.gob.ar/"
        url = f"{VEDI_API_BASE_URL}v3/Usuario/"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, token)
                response.raise_for_status()
                response_data = response.json()

                if not response_data.get("ok"):
                    raise ServiceException(
                        status_code=response.status_code,
                        detail=f"Error al obtener datos del usuario: {response_data.get('error')}"
                    )

                return response_data.get("return")
            except httpx.HTTPStatusError as e:
                raise ServiceException(
                    status_code=e.response.status_code,
                    detail=f"Error al obtener datos del usuario: {e.response.text}"
                )
            except Exception as e:
                raise ServiceException(
                    status_code=500,
                    detail=f"Error inesperado: {str(e)}"
                )

token_manager = TokenManager()