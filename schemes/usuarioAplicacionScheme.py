from datetime import  datetime
from pydantic import BaseModel, ConfigDict, Field


# Esquema para crear un usuario
class UsuarioAplicacionCreate(BaseModel):
    aplicacionId: int = Field(..., max_length=100, description="ID que proviene de la aplicacion")
    activo: bool = Field(True, description="Estado de la tabla")
    hashTabla: str = Field(None, max_length=100)


# Esquema para response de un usuario
class UsuarioAplicacionResponse(BaseModel):
    usuarioAplicacionId: int
    aplicacionId: int
    fechaCreacion: datetime
    activo: bool
    hashTabla: str

    model_config = ConfigDict(from_attributes=True)
