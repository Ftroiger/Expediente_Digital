from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func,Boolean
from db.database import Base

class Permiso(Base):
    __tablename__ = "Permiso"

    permisoId = Column(Integer, primary_key=True)
    nombrePermiso = Column(String(50), nullable=False)
    descripcionPermiso = Column(String(100), nullable=False)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True,nullable=False) 
    
    hashTabla = Column(String(100), nullable=False, unique=True)
