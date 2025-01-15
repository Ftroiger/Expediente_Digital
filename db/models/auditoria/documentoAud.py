from sqlalchemy import Column, Integer, String,TIMESTAMP,func
from sqlalchemy import Boolean, ForeignKey
from db.database import Base


class DocumentoAuditoria(Base):
    __tablename__ = 'DocumentoAuditoria'

    documentoAuditoriaId = Column(Integer, primary_key=True)
    ipAddress = Column(String(100))
    hostName = Column(String(100))
    userAgent = Column(String(100))
    fechaModificacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    operacionRealizada = Column(String(100), nullable=False)
    usuarioResponsableId = Column(Integer)
    usuariousuarioAplicacionResponsableId = Column(Integer)

    # Copia de tabla relacionada
    documentoId = Column(Integer, nullable=False)
    firmaDigitalId = Column(Integer, nullable=True)
    cddId = Column(String(50), nullable=False)  # ID en el centro de datos
    nombreArchivo = Column(String(255), nullable=False)
    tipoDocumento = Column(String(10), nullable=False)  # PDF, DOCX, XML
    versionDocumento = Column(Integer, nullable=False)
    cantPaginas = Column(Integer, nullable=False)
    fechaCreacion = Column(TIMESTAMP)
    hashTabla = Column(String(255), nullable=False)
    firmado = Column(Boolean, default=False)
    estado = Column(Boolean, default=False)  # Indica si el documento actual es la ultima version
    activo = Column(Boolean, default=True)  # Borrado logico
    documentoOrigenId = Column(Integer, nullable=True)
    qrId = Column(String(100), nullable=True)

