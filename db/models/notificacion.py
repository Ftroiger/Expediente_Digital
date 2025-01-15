from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.tipoNotificacion import TipoNotificacion

class Notificacion (Base):
    __tablename__ = 'Notificacion'
    notificacionId = Column(Integer, primary_key=True)
    usuarioNotificadoId = Column(Integer, ForeignKey('Usuario.usuarioId'), nullable=False)
    tipoNotificacionId = Column(Integer, ForeignKey('TipoNotificacion.tipoNotificacionId'), nullable=False)
    descripcionNotificacion = Column(String(255), nullable=False)
    usuarioAfectadoId = Column(Integer, nullable=True)
    leido = Column(Boolean, default=False, nullable=False)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True,nullable=False)
    hashTabla = Column(String(100), nullable=False, unique=True)

    usuario = relationship('Usuario')
    tipoNotificacion = relationship('TipoNotificacion')