from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# Esquema para crear un documento
class DocumentoCreateScheme(BaseModel):
    firmaDigitalId: Optional[int] = Field(None, description="Firma digital asociada al documento")
    cddId: Optional[str] = Field(None, description="Direccion de CDD")
    nombreArchivo: str = Field(..., max_length=255, description="Nombre asignado al archivo del documento")
    tipoDocumento: Optional[str] = Field(None, max_length=100, description="Tipo de archivo como PDF, DOCX, XML, etc.")
    cantPaginas: Optional[int] = Field(None, description="Cantidad de paginas en el documento")
    firmado: Optional[bool] = Field(None, description="True si se encuentra firmado el documento")
    estado: Optional[bool] = Field(None, description="Indica si el documento actual es la ultima version")
    documentoOrigenId: Optional[int] = Field(None, description="ID de la primera version del documento")
    activo: Optional[bool] = Field(True, description="Estado de la tabla")
    hashTabla: Optional[str] = Field(None, max_length=100)
    orden: int = Field(None, description="El orden del documento si pertenece a una lista de documentos")
    data: bytes = Field(None, description="La data del documento")

# Esquema response de un documento
class DocumentoResponse(BaseModel):
    documentoId: int
    firmaDigitalId: Optional[int] 
    cddId: Optional[str]
    nombreArchivo: str
    tipoDocumento: Optional[str]
    versionDocumento: Optional[int] 
    cantPaginas: Optional[int]
    fechaCreacion: Optional[datetime]
    firmado: Optional[bool] 
    estado: Optional[bool] 
    documentoOrigenId: Optional[int]
    #qrId: Optional[str] 
    activo: Optional[bool] 
    hashTabla: Optional[str]
    
    #qr: Optional[str] = None
    areaOrigenId: Optional[int] = None
    areaDestinoId: Optional[int] = None
    foliosInicial: Optional[int] = None
    foliosFinal: Optional[int] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class DocumentoQRCodeResponse(BaseModel):
    nombreArchivo: str
    qr: str  # El QR codificado como string
    documentoId: Optional[int] = None
    foliosInicial: Optional[int] = None
    folioFinal: Optional[int] = None
    areaOrigenId: Optional[int] = None
    areaDestinoId: Optional[int] = None
    cantPaginas: Optional[int] = None
    firmado: Optional[bool] = None
    usuarioCreador: int