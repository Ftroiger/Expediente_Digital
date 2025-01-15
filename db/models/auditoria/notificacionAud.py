from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean
from db.database import Base

class NotificacionAuditoria(Base):
    __tablename__ = 'NotificacionAuditoria'

    notificacionAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuariousuarioAplicacionResponsableId = Column(Integer)

    # Copia de tabla relacionada
    notificacionId = Column(Integer, nullable=False)
    usuarioNotificadoId = Column(Integer, nullable=False)
    tipoNotificacionId = Column(Integer, nullable=False)
    descripcionNotificacion = Column(String(255), nullable=False)
    usuarioAfectadoId = Column(Integer, nullable=True)
    leido = Column(Boolean, nullable=False)
    fechaCreacion = Column(TIMESTAMP, nullable=False)
    activo = Column(Boolean, default=True,nullable=False)
    hashTabla = Column(String(100), nullable=False)