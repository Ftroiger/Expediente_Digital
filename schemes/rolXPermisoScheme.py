from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class PermisosPorRolResponse(BaseModel):
    permisoId: int
    nombrePermiso: str
    descripcionPermiso: str
    fechaCreacion: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)

class RolXPermisoResponse(BaseModel):
    rolXPermisoId: int
    permisoId: int
    rolId: int
    fechaCreacion: datetime
    activo: bool 

class RolXPermisoCreate(BaseModel):
    permisoId: int
    rolId: int

    model_config = ConfigDict(from_attributes=True)