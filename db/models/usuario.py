from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, func
from db.database import Base

class Usuario(Base):
    __tablename__ = 'Usuario'

    usuarioId = Column(Integer, primary_key=True)
    cuilUsuario = Column(String(50))
    nombreUsuario = Column(String(50),nullable=False)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    fechaBaja = Column(TIMESTAMP,nullable=True)
    areaId = Column(Integer, nullable=True)
    aplicacionVediId = Column(Integer, unique=True, nullable=True)
    apiKey = Column(String(100), unique=True, nullable=True)
    usuarioAlta = Column(Integer, nullable=True)
    activo = Column(Boolean, nullable=False, default=True)
    hashTabla = Column(String(100), nullable=False)