from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class expedienteXNormaCreate(BaseModel):
    normaId: int = Field(..., description="Id de la norma")
    expedienteId: int = Field(..., description="Id del expediente")
    activo: bool = Field(True, description="Estado de la tabla")
    hashTabla: str = Field(None, max_length=100, description="Hash de la tupla")

    class Config:
        from_attributes = True

class expedienteXNormaResponse(BaseModel):
    expedienteXNormaId: int
    normaId: int
    expedienteId: int
    fechaAsociacion: datetime
    hashTabla: str
    activo: bool

    class Config:
        from_attributes = True

class actualizarExpedienteXNorma(BaseModel):
    normaId: int
    expedienteId: int
    activo: bool

    class Config:
        from_attributes = True