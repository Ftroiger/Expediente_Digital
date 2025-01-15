from sqlalchemy import Column, Integer, String, TIMESTAMP,func,Boolean
from sqlalchemy.orm import relationship
from db.database import Base


class ExpedienteXNormaAuditoria(Base):
    __tablename__ = 'ExpedienteXNormaAuditoria'

    expedienteXNormaAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    # Copia de tabla relacionada
    expedienteXNormaId =Column(Integer,nullable=False)
    
    fechaAsociacion = Column(TIMESTAMP,nullable=False)
    hashTabla = Column(String(100),nullable=False)
    activo = Column(Boolean,nullable=False,default=True)
    normaId = Column(Integer,nullable=False) 
    expedienteId = Column(Integer,nullable=False) 