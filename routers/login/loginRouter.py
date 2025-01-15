from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from servicios.vedi.vedi import LoginRequest, TokenManager
from utils.error.errors import ServiceException

router = APIRouter()
tokenManager = TokenManager()

# Model to receive data from the front
class LoginRequestModel(BaseModel):
    sessionId: str  # Expected data from the front

@router.post("/login/loginVeDi")
async def loginVedi(request: LoginRequest):

    sessionId = request.sessionId  # Convert to internal name
    
    if not sessionId:
        raise ServiceException(status_code=401, detail="Invalid token")
    
    try:
        # Get valid token
        token = await tokenManager.obtener_token_valido(sessionId)
    except Exception as e:
        raise ServiceException(status_code=401, detail=str(e))
    except ServiceException as e:
        raise e
    
    # Get user data with the generated token
    try:
        userVedi = await tokenManager.obtener_Datos_Usuario_Vedi(token)
    except Exception as e:
        raise ServiceException(status_code=401, detail="Error al obtener datos del usuario: " + str(e))
    except ServiceException as e:
        raise e
    
    # Validate user (placeholder)
    if userVedi.get("cuil") == "valid_cuil":
        return {
            "accessToken": tokenManager.token,       # Return the generated token
            "refreshToken": tokenManager.refresh_token  # Return the generated refresh token
        }
    else:
        raise ServiceException(status_code=401, detail="User invalid")
