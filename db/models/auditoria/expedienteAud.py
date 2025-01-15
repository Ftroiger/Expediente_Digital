from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func,Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.tipoExpediente import TipoExpediente



class ExpedienteAuditoria(Base):
    __tablename__ = 'ExpedienteAuditoria'

    expedienteAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuariousuarioAplicacionResponsableId = Column(Integer)

    # Copia de tabla relacionada
    expedienteId=Column(Integer,nullable=False)
    tipoExpedienteId=Column(Integer,nullable=False)
    expedientePadreId=Column(Integer,nullable=True)
    numeroExpediente= Column(String(50),nullable=False)
    areaIniciadoraId=Column(Integer,nullable=False)
    usuarioCreadorFisicoId=Column(Integer,nullable=False)
    usuarioCreadorAplicacionId =Column(Integer, nullable=False)
    asuntoExpediente = Column(String(255),nullable=False)
    fechaCreacion=Column(TIMESTAMP,nullable=False)
    fechaUltimoMovimiento=Column(TIMESTAMP)
    visibilidadExpediente=Column(String(50), nullable=False)
    temaNombre = Column(String(100), nullable=False)
    activo = Column(Boolean,nullable=False,default=True)
    hashTabla = Column(String(100),nullable=False)
    areaActualidadId = Column(Integer,nullable=True)
    foliosApertura = Column(Integer,nullable=False)
    foliosActuales = Column(Integer,nullable=True)
    documentoSiradId = Column(Integer,nullable=True)
