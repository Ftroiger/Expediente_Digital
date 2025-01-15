from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, PydanticUserError
from typing import Optional

# Esquema para crear un permiso
class PermisoCreate(BaseModel):
    nombrePermiso: str = Field(..., max_length=50, description="Permiso sobre el expediente")
    descripcionPermiso: str = Field(..., max_length=100, description="Descripcion sobre los permisos")
    #activo: bool = Field(True, description="Estado de la tabla")
    nombreRol: str = Field(..., max_length=50, description="Nombre del rol")

# Esquema response para un permiso
class PermisoResponse(BaseModel):
    permisoId: int
    nombrePermiso: str
    descripcionPermiso: str
    fechaCreacion: Optional[datetime]
    activo: bool

    model_config = ConfigDict(from_attributes=True)