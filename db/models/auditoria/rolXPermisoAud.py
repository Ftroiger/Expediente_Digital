from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey
from db.database import Base


class RolXusuarioAuditoria(Base):
    __tablename__ = 'RolXusuarioAuditoria'

    rolXUsuarioAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    rolXPermisoId = Column(Integer, nullable=False)
    permisoId = Column(Integer, nullable=False)
    rolId = Column(Integer, nullable=False)
    fechaCreacion = Column(TIMESTAMP, nullable=False)
    activo = Column(Boolean, nullable=False) # Borrado logico
    hashTabla = Column(String(100), nullable=False)
