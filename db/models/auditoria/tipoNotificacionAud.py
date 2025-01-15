from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean
from db.database import Base

class TipoNotificacionAuditoria(Base):
    __tablename__ = 'TipoNotificacionAuditoria'

    notificacionAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuariousuarioAplicacionResponsableId = Column(Integer)

    #Copia de tabla relacionada
    tipoNotificacionId = Column(Integer, primary_key=True)
    nombreTipoNotificacion= Column(String(50), nullable=False)
    descripcionTipoNotificacion = Column(String(255), nullable=False)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True,nullable=False)
    hashTabla = Column(String(100), nullable=False)