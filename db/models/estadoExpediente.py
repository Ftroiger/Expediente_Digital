from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func, Boolean
from db.database import Base

class EstadoExpediente(Base):
    __tablename__ = "EstadoExpediente"

    estadoExpedienteId = Column(Integer, primary_key=True)
    nombreEstadoExpediente = Column(String(50), unique=True, nullable=False)
    descripcionEstadoExpediente = Column(String(255),nullable=False)

    activo = Column(Boolean, default=True) 
    hashTabla = Column(String(100), nullable=False, unique=True)
    
