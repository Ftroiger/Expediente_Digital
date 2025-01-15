from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey
from db.database import Base


class DocumentoXMovimientoAuditoria(Base):
    __tablename__ = 'DocumentoXMovimientoAuditoria'

    documentoXMovimientoAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuarioAplicacionResponsableId = Column(Integer)

    #Copia de los datos de la tabla

    documentoXMovimientoId =Column(Integer,nullable = False)
    movimientoId = Column(Integer,nullable=False) 
    documentoId = Column(Integer,nullable=False) 
    fechaAsociacion = Column(TIMESTAMP,nullable=False)
    foliosInicial = Column(Integer,nullable=False)
    foliosFinal = Column(Integer,nullable=False)
    activo = Column(Boolean,nullable=False)
    hashTabla = Column(String(100),nullable=False)