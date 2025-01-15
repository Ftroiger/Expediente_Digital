from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.expediente import Expediente
from db.models.usuario import Usuario

class Movimiento(Base):
    __tablename__ = "Movimiento"

    movimientoId = Column(Integer, primary_key=True, autoincrement=True)
    tramiteId = Column(Integer, nullable=False)
    expedienteId = Column(Integer, ForeignKey('Expediente.expedienteId'), nullable=False)
    usuarioFisicoId = Column(Integer, ForeignKey('Usuario.usuarioId'), nullable=False)
    usuarioAplicacionId = Column(Integer, ForeignKey('Usuario.usuarioId'), nullable=False)
    areaOrigenId = Column(Integer, nullable=False)
    areaDestinoId = Column(Integer, nullable=True)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    observacionMovimiento = Column(Text, nullable=True)
    activo = Column(Boolean, default=True) 
    hashTabla = Column(String(100), nullable=False)

    expediente = relationship('Expediente')
    usuarioAplicacion = relationship('Usuario', foreign_keys=[usuarioAplicacionId])
    usuarioFisico = relationship('Usuario', foreign_keys=[usuarioFisicoId])
