from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Rol(Base):
    __tablename__ = "Rol"

    rolId = Column(Integer, primary_key=True, nullable=False)
    nombreRol = Column(String(50), nullable=False)
    descripcionRol = Column(String(100), nullable=False)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True) # Borrado logico
    hashTabla = Column(String(100), nullable=False)