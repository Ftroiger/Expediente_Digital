from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func,Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.norma import Norma
from db.models.expediente import Expediente


class ExpedienteXNorma(Base):
    __tablename__ = 'ExpedienteXNorma'
    __table_args__ = {'extend_existing': True}

    expedienteXNormaId =Column(Integer,primary_key=True)
    
    fechaAsociacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    hashTabla = Column(String(100),nullable=False)
    activo = Column(Boolean,nullable=False,default=True)

    normaId = Column(Integer,ForeignKey('Norma.normaId'),nullable=False) 
    norma = relationship('Norma')
    expedienteId = Column(Integer,ForeignKey('Expediente.expedienteId'),nullable=False) 
    expediente = relationship('Expediente')