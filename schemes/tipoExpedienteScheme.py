from pydantic import BaseModel, Field

# Esquema para crear un expediente
class TipoExpedienteCreate(BaseModel):
    nombreTipoExpediente: str = Field(..., max_length=50)
    descripcionTipoExpediente: str = Field(..., max_length=255)
    activo: bool = Field(True)
    hashTabla: str = Field(None, max_length=100)

    class Config:
        from_attributes = True      

# Esquema para obtener un tipo de expediente
class TipoExpedienteResponse(BaseModel):
    tipoExpedienteId: int 
    nombreTipoExpediente: str 
    descripcionTipoExpediente: str 
    activo: bool 
    hashTabla: str 

    class Config:
        from_attributes = True


# Esquema para actualizar un expediente
class ActualizarTipoExpediente(BaseModel):
    tipoExpedienteId: int 
    nombreTipoExpediente: str 
    descripcionTipoExpediente: str 
    activo: bool 
    hashTabla: str 
    
    class Config:
        from_attributes = True