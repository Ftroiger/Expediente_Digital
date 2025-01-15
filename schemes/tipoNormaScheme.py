from pydantic import BaseModel, Field, ConfigDict

# Esquema para crear un tipo de norma
class TipoNormaCreate(BaseModel):
    nombreTipoNorma: str = Field(..., max_length=50)
    descripcionTipoNorma: str = Field(None, max_length=255)
    activo: bool = Field(True, description="Estado de la tabla")
    hashTabla: str = Field(None, max_length=100)

    class Config:
        from_attributes = True

class TipoNormaResponse(BaseModel):
    tipoNormaId: int
    nombreTipoNorma: str
    descripcionTipoNorma: str
    activo: bool
    hashTabla: str

    class Config:
        from_attributes = True


# class ObtenerTipoNormaPorId(BaseModel):
#     tipoNormaId: int

#     class Config:
#         from_attributes = True


class ActualizarTipoNorma(BaseModel):
    nombreTipoNorma: str
    descripcionTipoNorma: str
    activo: bool

    class Config:
        from_attributes = True

# class EliminarTipoNorma(BaseModel):
#     tipoNormaId: int

#     class Config:
#         from_attributes = True