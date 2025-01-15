from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from schemes.documentoScheme import DocumentoCreateScheme

# Esquema response de un movimiento baseado en el modelo de la base de datos
class MovimientoResponse(BaseModel):
    movimientoId: int = Field(..., description="ID único del movimiento")
    tramiteId: int = Field(..., description="ID del trámite asociado")
    expedienteId: int = Field(..., description="ID del expediente asociado")
    usuarioFisicoId: int = Field(..., description="ID del usuario de la aplicación")
    usuarioAplicacionId : int = Field(..., description="ID del usuario de la aplicación")
    areaOrigenId: int = Field(..., description="ID del área de origen")
    areaDestinoId: int = Field(..., description="ID del área de destino actual")
    fechaCreacion: Optional[datetime] = Field(None, description="Fecha de creación del movimiento")
    observacionMovimiento: str = Field(..., description="Observaciones sobre el movimiento")
    activo: bool = Field(True, description="Estado de la tabla")
    hashTabla: Optional[str] = Field(None, max_length=100, description="Hash de la tabla para control de concurrencia")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Esquema para actualizar un movimiento
class movimientoUpdate(BaseModel):
    observacionMovimiento: str
    activo: bool
    hashTabla: str

    model_config = ConfigDict(from_attributes=True)

class MovimientoCreateScheme(BaseModel):
    
    # Datos para la tabla Movimiento
    tramiteId: int = Field(..., description="ID del indice del tramite")
    # numeroExpediente: Optional[str] = Field(..., description="Numero de expediente asociado al movimiento")
    #usuarioAplicacionId: int = Field(..., description="Usuario que realizo movimiento")
    areaOrigenId: int = Field(..., description="Area previa a la actual")
    areasDestinoId: list[int] = Field(..., description="Areas actuales")
    observacionMovimiento: Optional[str] = Field(..., description="Observaciones sobre el movimiento")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }