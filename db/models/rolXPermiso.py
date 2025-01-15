from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class RolXPermiso(Base):
    __tablename__ = "RolXPermiso"

    rolXPermisoId = Column(Integer, primary_key=True, nullable=False)
    permisoId = Column(Integer, ForeignKey('Permiso.permisoId'))
    rolId = Column(Integer, ForeignKey('Rol.rolId'))
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True) # Borrado logico
    hashTabla = Column(String(100), nullable=False)

    permiso = relationship("Permiso")
    rol = relationship("Rol")