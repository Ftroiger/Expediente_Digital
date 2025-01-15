from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.usuario import Usuario
from db.models.rol import Rol

class RolXUsuario(Base):
    __tablename__ = "RolXUsuario"
    __table_args__ = {'extend_existing': True}

    rolXUsuarioId = Column(Integer, primary_key=True)
    usuarioId = Column(Integer, ForeignKey("Usuario.usuarioId"), nullable=False)
    usuario = relationship("Usuario")
    rolId = Column(Integer, ForeignKey("Rol.rolId"), nullable=False)
    rol = relationship("Rol")

    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    hashTabla = Column(String(100), nullable=False, unique=True)
