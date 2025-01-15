from sqlalchemy import Column, Integer, Boolean, String,TIMESTAMP,func
from db.database import Base

class TipoExpedienteAuditoria(Base):
    __tablename__ = 'TipoExpedienteAuditoria'

    tipoExpedienteAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    tipoExpedienteId = Column(Integer, nullable=False)
    nombreTipoExpediente = Column(String(50), nullable=False)
    descripcionTipoExpediente = Column(String(255))
    activo = Column(Boolean, nullable=False ,default=True) 
    hashTabla = Column(String(100), nullable=False)