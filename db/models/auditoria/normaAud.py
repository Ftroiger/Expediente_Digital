from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey, Text
from db.database import Base


class NormaAuditoria(Base):
    __tablename__ = 'NormaAuditoria'

    normaAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    # Copia de tabla relacionada
    normaId = Column(Integer, nullable=False)
    tipoNormaId = Column(Integer, nullable=False)
    numeroNorma = Column(String(50), nullable=False)
    descripcionNorma = Column(String(255), nullable=True)
    fechaCreacion = Column(TIMESTAMP, nullable=False)
    normaCddId = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)
    hashTabla = Column(String(100), nullable=False)