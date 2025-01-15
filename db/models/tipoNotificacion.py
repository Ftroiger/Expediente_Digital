from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey, Text
from db.database import Base

class TipoNotificacion(Base):
    __tablename__ = 'TipoNotificacion'

    tipoNotificacionId = Column(Integer, primary_key=True)
    nombreTipoNotificacion = Column(String(50), nullable=False)
    descripcionTipoNotificacion = Column(String(255), nullable=False)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True,nullable=False)
    hashTabla = Column(String(100), nullable=False)