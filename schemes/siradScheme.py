from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from utils.error.errors import ErrorResponse
from datetime import datetime

# ----- SIRAD - Cambiar según las especificaciones del servicio -----

# Esquema para el representante
class RepresentanteScheme(BaseModel):
    Sexo: str = Field(..., description="Sexo del representante", required=True)
    Nombre: str = Field(..., description="Nombre del representante", required=True)
    Apellido: str = Field(..., description="Apellido del representante", required=True)
    NroDocumento: str = Field(..., description="DNI del representante", required=True)

    @field_validator("Sexo")
    def checkSexo(cls, v):
        if v not in ["M", "F", "X","Otro"]:
            raise ValueError("El sexo debe ser M , F, X, Otro")
        return v
    
# Esquema para la sucursal
class SucursalScheme(BaseModel):
    NomenclaturaCatastral: str = Field(..., description="Nomenclatura catastral de la sucursal")
    Representante: RepresentanteScheme = Field(..., description="Representante de la sucursal")

# Esquema para el iniciador persona jurídica
class IniciadorPersonaJuridicaScheme(BaseModel):
    Cuit: str = Field(..., description="CUIT del iniciador", required=True, max_length=11)
    RazonSocial: str = Field(..., description="Razón social del iniciador")
    Sucursal: SucursalScheme = Field(..., description="Sucursal del iniciador")
    
    @field_validator("Cuit")
    def checkCuit(cls, v):
        if len(str(v)) != 11:
            raise ValueError("El CUIT debe tener 11 dígitos sin guiones")
        return v

# Esquema para el iniciador persona física
class IniciadorPersonaFisicaScheme(BaseModel):
    Sexo: str = Field(..., description="Sexo del iniciador", required=True)
    Nombre: str = Field(..., description="Nombre del iniciador", required=True)
    Apellido: str = Field(..., description="Apellido del iniciador", required=True)
    NroDocumento: str = Field(..., description="DNI del iniciador", required=True)

    @field_validator("Sexo")
    def checkSexo(cls, v):
        if v not in ["M", "F", "X","Otro"]:
            raise ValueError("El sexo debe ser M , F, X, Otro")
        return v

# Esquema para la llamada del API a SIRAD
class CrearDocumentoPorEntidadScheme(BaseModel):
    IdTema: int = Field(..., description="ID del tema", requiered=True,ge=1)
    Asunto: str = Field(..., description="Asunto del expediente", requiered=True)
    Observaciones: Optional[str] = Field(..., description="Observaciones del expediente")

    IniciadorPersonaFisica: Optional[IniciadorPersonaFisicaScheme] = None
    IniciadorPersonaJuridica: Optional[IniciadorPersonaJuridicaScheme] = None

    @classmethod
    def validate(cls, values):
        if values.get("IniciadorPersonaFisica") is None and values.get("IniciadorPersonaJuridica") is None:
            raise ValueError("Debe ingresar un Iniciador Física o un Iniciador Jurídica")

        if values.get("IniciadorPersonaFisica") and values.get("IniciadorPersonaJuridica"):
            raise ValueError("Debe ingresar un Iniciador Física o un Iniciador Jurídica, no ambos")
        return values

class TemaScheme(BaseModel):
    Nombre: str = Field(..., description="Nombre del tema")
    Descripcion: Optional[str] = Field(None, description="Descripción del tema")
    Observaciones: Optional[str] = Field(None, description="Observaciones del tema")
    FechaInicioVigencia: Optional[datetime] = Field(None, description="Fecha de inicio de vigencia")
    FechaFinVigencia: Optional[datetime] = Field(None, description="Fecha de fin de vigencia")
    Id: int = Field(..., description="ID del tema")
    FechaAlta: Optional[datetime] = Field(None, description="Fecha de alta")
    FechaBaja: Optional[datetime] = Field(None, description="Fecha de baja")