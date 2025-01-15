from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.expediente import Expediente
from db.models.estadoExpediente import EstadoExpediente

class HistorialEstadoExpediente(Base):
    __tablename__ = "HistorialEstadoExpediente"

    historialEstadoExpedienteId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    estadoExpedienteId = Column(Integer, ForeignKey('EstadoExpediente.estadoExpedienteId'), nullable=False)
    expedienteId = Column(Integer, ForeignKey('Expediente.expedienteId'), nullable=False)
    fechaDesde = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    fechaHasta = Column(TIMESTAMP, nullable=True)
    hashTabla = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True) 

    estadoExpediente = relationship('EstadoExpediente')
    expediente = relationship('Expediente')