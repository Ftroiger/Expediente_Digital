from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from db.database import Base

class TipoNormaAuditoria(Base):
    __tablename__ = "TipoNormaAuditoria"

    tipoNormaAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    tipoNormaId = Column(Integer, nullable=False)
    nombreTipoNorma = Column(String(50), nullable=False)
    descripcionTipoNorma = Column(String(255), nullable=True)
    activo = Column(Boolean, nullable=False,default=True)
    hashTabla = Column(String(100), nullable=False)