from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class NormaCreate(BaseModel):
    tipoNormaId: int = Field(..., description="Id del tipo de norma")
    numeroNorma: str = Field(..., max_length=50, description="Número de la norma")
    descripcionNorma: str = Field(None, max_length=255, description="Descripción de la norma")
    normaCddId: int = Field(..., description="Id de la norma en CDD")
    activo: bool = Field(True, description="Estado de la tabla")
    hashTabla: str = Field(None, max_length=100, description="Hash de la tupla")

    class Config:
        from_attributes = True

class NormaResponse(BaseModel):
    normaId: int
    tipoNormaId: int
    numeroNorma: str
    descripcionNorma: str
    fechaCreacion: datetime  # Modified to datetime to match TIMESTAMP type
    normaCddId: int
    activo: bool
    hashTabla: str

    class Config:
        from_attributes = True

# class BuscarNormaPorId(BaseModel):
#     normaId: int

#     class Config:
#         from_attributes = True

class ActualizarNorma(BaseModel):
    tipoNormaId: int
    numeroNorma: str
    descripcionNorma: str
    normaCddId: int
    activo: bool

    class Config:
        from_attributes = True

# class EliminarNorma(BaseModel):
#     normaId: int

#     class Config:
#         from_attributes = True
