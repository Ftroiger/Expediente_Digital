from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey, Text
from db.database import Base

class UsuarioAuditoria(Base):
    __tablename__ = 'UsuarioAuditoria'

    usuarioAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    # Copia de tabla relacionada
    usuarioId = Column(Integer, nullable=False)
    cuilUsuario = Column(String(50), nullable=True)
    nombreUsuario = Column(String(50), nullable=False)
    fechaCreacion = Column(TIMESTAMP, nullable=False)
    fechaBaja = Column(TIMESTAMP, nullable=True)
    areaId = Column(Integer, nullable=True)
    aplicacionVediId = Column(Integer, nullable=True)
    apiKey = Column(String(100), nullable=True)
    usuarioAlta = Column(Integer, nullable=True)
    activo = Column(Boolean, default=True)
    hashTabla = Column(String(100), nullable=False)