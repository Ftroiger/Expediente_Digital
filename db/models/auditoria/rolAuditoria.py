from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey
from db.database import Base

class RolAuditoria(Base):
    __tablename__ = 'RolAuditoria'

    rolAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    rolId = Column(Integer, nullable=False)
    nombreRol = Column(String(50), nullable=False)
    descripcionRol = Column(String(100), nullable=False)
    fechaCreacion = Column(TIMESTAMP, nullable=False)
    activo = Column(Boolean, nullable=False) # Borrado logico
    hashTabla = Column(String(100), nullable=False)