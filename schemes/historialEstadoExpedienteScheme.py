from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional 
# Esquema para crear un historial estado expediente]

class HistorialEstadoExpedienteCreate(BaseModel):
    estadoId:  int = Field
    expedienteId:  int
    activo: bool = Field(True,description="Estado de la tabla")
    hashTabla: str = Field(None,max_length=100)

    class Config:
        from_attributes = True

class HistorialEstadoExpedienteResponse(BaseModel):
    historialEstadoExpedienteId: int
    estadoId: int = Field(..., alias='estadoExpedienteId')
    expedienteId: int
    fechaDesde: Optional[datetime]
    fechaHasta: Optional[datetime]
    activo: bool
    hashTabla : str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Convertir datetime a string en formato ISO
            }



