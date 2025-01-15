from sqlalchemy import Column, Integer, Boolean, String,TIMESTAMP,func
from db.database import Base

class PermisoAuditoria(Base):
    __tablename__ = "PermisoAuditoria"

    permisoAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    permisoId = Column(Integer, nullable=False)
    nombrePermiso = Column(String(50), nullable=False)
    descripcionPermiso = Column(String(100), nullable=False)
    fechaCreacion = Column(TIMESTAMP, nullable=False)
    activo = Column(Boolean, default=True,nullable=False) 
    hashTabla = Column(String(100), nullable=False)