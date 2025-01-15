from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class estadoExpedienteCreate(BaseModel):
    nombreEstadoExpediente: str = Field(..., max_length=50, description="Nombre del estado del expediente")
    descripcionEstadoExpediente: str = Field(..., max_length=255, description="Descripcion del estado del expediente")
    activo: bool = Field(True, description="Estado del expediente")

    class Config:
        from_attributes = True


class estadoExpedienteResponse(BaseModel):
    estadoExpedienteId: int
    nombreEstadoExpediente: str
    descripcionEstadoExpediente: str
    activo: bool

    class Config:
        from_attributes = True

class estadoExpedienteUpdate(BaseModel):
    nombreEstadoExpediente: str
    descripcionEstadoExpediente: str
    activo: bool

    class Config:
        from_attributes = True

class estadoExpedienteDelete(BaseModel):
    estadoExpedienteId: int

    class Config:
        from_attributes = True
