from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func, Boolean
from db.database import Base

class EstadoExpedienteAuditoria(Base):
    __tablename__ = "EstadoExpedienteAuditoria"

    estadoExpedienteAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionId = Column(Integer)

    # Copia de tabla relacionada
    estadoExpedienteId = Column(Integer,nullable=False)
    nombreEstadoExpediente = Column(String(50), nullable=False)
    descripcionEstadoExpediente = Column(String(255),nullable=False)
    activo = Column(Boolean, default=True) 
    hashTabla = Column(String(100), nullable=False)
    
    