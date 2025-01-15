from sqlalchemy import Column, Integer, Boolean, String,TIMESTAMP,func
from db.database import Base

class HistorialEstadoExpedienteAuditoria(Base):
    __tablename__ = 'HistorialEstadoExpedienteAuditoria'

    historialEstadoExpedienteAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    historialEstadoExpedienteId = Column(Integer, autoincrement=True, nullable=False)
    estadoExpedienteId = Column(Integer, nullable=False)
    expedienteId = Column(Integer, nullable=False)
    fechaDesde = Column(TIMESTAMP, nullable=False)
    fechaHasta = Column(TIMESTAMP, nullable=True)
    hashTabla = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True) 