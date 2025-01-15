from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class NotificacionResponse(BaseModel):
    notificacionId: int
    usuarioNotificadoId: int
    tipoNotificacionId: int
    descripcionNotificacion: str
    usuarioAfectadoId: int
    leido: bool
    fechaCreacion: datetime
    activo: bool
    hashTabla: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }