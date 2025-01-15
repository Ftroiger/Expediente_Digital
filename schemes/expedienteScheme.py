from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, Union
from datetime import datetime
from schemes.siradScheme import CrearDocumentoPorEntidadScheme
from schemes.documentoScheme import DocumentoCreateScheme

# Esquema para obtener un expediente
class ExpedienteResponse(BaseModel):
    expedienteId: int = Field(..., description="ID del expediente",ge=1)
    tipoExpedienteId: int = Field(..., description="ID del tipo de expediente",ge=1)
    expedientePadreId: Optional[int] = Field(None, description="ID del expediente padre")
    numeroExpediente: str = Field(..., description="Número del expediente")
    areaIniciadoraId: int = Field(..., description="ID del área iniciadora del expediente",ge=1)
    usuarioCreadorFisicoId: int = Field(..., description="ID del usuario creador fisico (persona) del expediente",ge=1)
    usuarioCreadorAplicacionId: int = Field(..., description="ID del usuario creador aplicación (sistema) del expediente",ge=1)
    asuntoExpediente: str = Field(..., description="Asunto del expediente")
    fechaCreacion: Optional [datetime] = Field(None, description="Fecha de creación del expediente")
    fechaUltimoMovimiento: Optional [datetime] = Field(None, description="Fecha del último movimiento del expediente")
    visibilidadExpediente: Literal ["Público", "Privado", "MuyPrivado"] = Field(..., description="Visibilidad del expediente")
    activo: bool = Field(..., description="Estado del expediente")
    temaNombre: Optional[str] = Field(..., description="Nombre del tema del expediente")
    hashTabla: str = Field(..., description="Hash de la tabla del expediente")
    areaActualidadId: Optional[int] = Field(None, description="ID del área actualidad del expediente")
    foliosApertura: int = Field(..., description="Folios de apertura del expediente",ge = 0)
    foliosActuales: Optional[int] = Field(None, description="Folios actuales del expediente", ge = 0)
    documentoSiradId: Optional[int] = Field(None, description="ID del documento en SIRAD")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Esquema para actualizar un expediente
class ActualizarExpediente(BaseModel):
    tipoExpedienteId: int 
    expedientePadreId: int 
    numeroExpediente: str 
    areaIniciadoraId: int 
    usuarioCreadorFisicoId: int
    usuarioCreadorAplicacionId: int 
    asuntoExpediente: str 
    visibilidadExpediente: str 
    fechaCreacion: Optional [datetime]
    fechaUltimoMovimiento: Optional [datetime]
    activo: bool 
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Esquema para crear un expediente INCLUYENDO DATOS PARA MOVIMIENTO Y SIRAD
class ExpedienteCreateScheme(BaseModel):

    # Datos obligatorios para la tabla Expediente
    expedientePadreId: Optional[int] = Field(None, description="ID del expediente padre")
    visibilidadExpediente: Literal["Público","Privado", "MuyPrivado"] = Field(..., description="Visibilidad del expediente: (Público, Privado, MuyPrivado)",required=True)
    areaIniciadoraId: int = Field(..., description="ID del área iniciadora del expediente",required=True,ge=1)
    #usuarioCreadorFisicoId: int = Field(..., description="ID del usuario creador del expediente",required=True,ge=1)
    #usuarioCreadorAplicacionId: int = Field(..., description="ID del usuario creador del expediente",required=True,ge=1)
    temaNombre: str = Field(..., description="Nombre del tema del expediente",required=True)

    # Datos obligatorios para la tabla Movimiento
    tramiteId: int = Field(..., description="ID del trámite del expediente",required=True,ge=1)
    #areaDestinoId: int = Field(..., description="ID del área destino del expediente")

    # PDF en bytes
    #NotaPDF: bytes = Field(..., description="Nota del expediente en formato PDF")

    #documentos: list[DocumentoCreateScheme] = Field(..., description="Lista de documentos para el expediente")

    # SIRAD
    sirad: CrearDocumentoPorEntidadScheme = Field(..., description="Datos para la creación del documento en SIRAD",required=True)

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Convertir datetime a string en formato ISO
        }

class OrganigramaEntry(BaseModel):
    id_unidad: Optional[int]
    unidad: Optional[str]
    id_cerrojo: Optional[int]
    tipo: Optional[str]
    ubicacion: Optional[str]
    externa: Optional[bool]
    mesa: Optional[str]  # Definir como string
    id_unidad_superior: Optional[int]
    unidad_superior: Optional[str]
    id_cerrojo_superior: Optional[int]
    tipo_superior: Optional[str]
    ubicacion_superior: Optional[str]
    externa_superior: Optional[bool]
    mesa_superior: Optional[str]

    @field_validator("mesa_superior", mode="before")
    def validate_mesa_superior(cls, value):
        # Convertir cualquier número entero en una cadena
        if value is not None:
            return str(value)
        return value

    @field_validator("mesa", mode="before")
    def validate_mesa(cls, value):
        # Convertir cualquier número entero en una cadena
        if value is not None:
            return str(value)
        return value

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Convertir datetime a string en formato ISO
        }