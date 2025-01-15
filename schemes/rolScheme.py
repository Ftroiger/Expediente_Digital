from typing import List
from pydantic import BaseModel, Field, ConfigDict

from db.models.permiso import Permiso

class rolCreate(BaseModel):
    nombreRol: str = Field(...,max_length=50, description="Nombre del rol que se le asigna al usuario")
    descripcionRol: str = Field(..., max_length=100, description="Descripcion del rol")

class rolResponse(BaseModel):
    rolId: int
    nombreRol: str
    descripcionRol: str
    activo: bool 
    hashTabla: str 

    model_config = ConfigDict(from_attributes=True)
