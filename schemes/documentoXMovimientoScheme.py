from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class documentoXMovimientoCreate(BaseModel):
    movimientoId: int = Field(..., description="Id del movimiento")
    documentoId: int = Field(..., description="Id del documento")
    # fechaAsociacion: datetime = Field(..., description="Fecha de asociacion")
    foliosInicial: int = Field(..., description="Folio inicial")
    foliosFinal: int = Field(..., description="Folio final")
    activo: bool = Field(True, description="Activo")

    class Config:
        from_attributes = True

class documentoXMovimientoResponse(BaseModel):
    documentoXMovimientoId: int
    movimientoId: int
    documentoId: int
    fechaAsociacion: datetime
    foliosInicial: Optional[int]
    foliosFinal: Optional[int]
    activo: bool

    class Config:
        from_attributes = True

class documentoXMovimientoUpdate(BaseModel):
    movimientoId: int
    documentoId: int
    # fechaAsociacion: datetime
    foliosInicial: int
    foliosFinal: int
    activo: bool

    class Config:
        from_attributes = True