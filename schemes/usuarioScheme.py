from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# UsuarioCreate: Modelo de datos para la creación de un usuario
class UsuarioCreate(BaseModel):
    nombreUsuario: str = Field(..., max_length=50, description="Nombre del usuario")
    cuilUsuario: str = Field(..., max_length=50, description="CUIL del usuario")
    # fechaCreacion: Optional [datetime] = Field(None, description="Fecha de creación del usuario")
    # fechaBaja: Optional [datetime] = Field(None, description="Fecha de baja del usuario")
    #aplicacionVediId: Optional [int] = Field(None, description="Aplicación a la que pertenece el usuario")
    #apiKey: Optional [str] = Field(None, max_length=100, description="Clave de acceso del usuario")
    areaId: Optional [int] = Field(None, description="ID del área del usuario")
    # activo: Optional[bool] = Field(True, description="Estado de la tabla")
    # hashTabla: Optional[str] = Field(None, max_length=100)

# UsuarioResponse: Modelo de datos para la respuesta de un usuario
class UsuarioResponse(BaseModel):
    usuarioId: int
    cuilUsuario: Optional[str]
    nombreUsuario: str
    fechaCreacion: Optional[datetime]
    fechaBaja: Optional[datetime] = None 
    areaId: Optional[int]
    usuarioAlta: Optional[int]
    aplicacionVediId: Optional[int]
    apiKey: Optional[str]
    activo: Optional[bool]
    
    hashTabla: Optional[str]
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# UsuarioAplicacionCreate: Modelo de datos para la creación de un usuario con rol aplicación
class UsuarioAplicacionCreate(BaseModel):
    nombreUsuario: str = Field(..., max_length=50, description="Nombre del usuario")
    areaId: int = Field(..., description="ID del área del usuario")
    aplicacionVediId: int = Field(..., description="ID de la aplicación VEDI")

# UsuarioAdministradorCreate: Modelo de datos para la creación de un usuario con rol administrador
class UsuarioAdministradorCreate(BaseModel):
    cuilUsuario: str = Field(..., max_length=50, description="CUIL del usuario")
    nombreUsuario: str = Field(..., max_length=50, description="Nombre del usuario")
    areaId: int = Field(..., description="ID del área del usuario")

class UsuarioSuperAdminCreate(BaseModel):
    cuilUsuario: str = Field(..., max_length=100, description="CUIL del usuario")
    nombreUsuario: str = Field(..., max_length=100, description="Nombre del usuario")
    areaId: int = Field(..., description="ID del área del usuario")

class UsuarioAplicacionResponse(BaseModel):
    usuarioId: int
    cuilUsuario: Optional[str]
    nombreUsuario: str
    areaId: int
    aplicacionVediId: int
    apiKey: str
    activo: bool
    fechaCreacion: datetime
    fechaBaja: Optional[datetime]
    hashTabla: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UsuarioNotificacionCreate(BaseModel):
    descripcionNotificacion: str = Field(..., max_length=255, description="Descripción de la notificación")
    usuarioAfectadoId: Optional[int] = Field(None, description="ID del usuario afectado")
