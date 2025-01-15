from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey, Text
from db.database import Base


class MovimientoAuditoria(Base):
    __tablename__ = 'MovimientoAuditoria'

    movimientoAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    # Copia de tabla relacionada
    movimientoId = Column(Integer, nullable=False)
    tramiteId = Column(Integer, nullable=False)
    expedienteId = Column(Integer, nullable=False)
    usuarioFisicoId = Column(Integer, nullable=False)
    usuarioAplicacionId = Column(Integer, nullable=False)
    areaOrigenId = Column(Integer, nullable=False)
    areaDestinoId = Column(Integer, nullable=True)
    fechaCreacion = Column(TIMESTAMP, nullable=False)
    observacionMovimiento = Column(Text, nullable=True)
    activo = Column(Boolean, default=True) 
    hashTabla = Column(String(100), nullable=False)


