from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func,Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.tipoExpediente import TipoExpediente
from db.models.usuario import Usuario



class Expediente (Base):
    __tablename__ = 'Expediente'

    expedienteId=Column(Integer,primary_key=True)
    tipoExpedienteId=Column(Integer,ForeignKey("TipoExpediente.tipoExpedienteId"),nullable=False)
    expedientePadreId=Column(Integer, nullable=True)
    numeroExpediente= Column(String(50), unique=True,nullable=False)
    areaIniciadoraId=Column(Integer,nullable=False)
    usuarioCreadorFisicoId = Column (Integer, nullable=False)
    usuarioCreadorAplicacionId = Column (Integer, nullable=False)
    asuntoExpediente = Column(String(255),nullable=False)
    fechaCreacion=Column(TIMESTAMP, server_default=func.now(), nullable=False)
    fechaUltimoMovimiento=Column(TIMESTAMP)
    visibilidadExpediente=Column(String(50), nullable=False,default='Publica')
    activo = Column(Boolean,nullable=False,default=True)
    temaNombre = Column(String(100), nullable=False)
    hashTabla = Column(String(100),nullable=False)

    # Agregos
    areaActualidadId = Column(Integer,nullable=True)
    foliosApertura = Column(Integer,nullable=False)
    foliosActuales = Column(Integer,nullable=True)
    documentoSiradId = Column(Integer,nullable=True)


    tipoExpediente = relationship('TipoExpediente')

    @classmethod
    def exists(cls, session, expedienteId):
        return session.query(cls).filter_by(expedienteId=expedienteId).first() is not None