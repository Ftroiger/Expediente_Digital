from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean,func
from sqlalchemy.orm import relationship
from db.database import Base

class Documento(Base):
    __tablename__ = "Documento"

    documentoId = Column(Integer, primary_key=True, nullable=False)
    firmaDigitalId = Column(Integer, nullable=True)
    cddId = Column(String(50),unique=True, nullable=False) #ID en el centro de datos
    nombreArchivo = Column(String(255), nullable=False)
    tipoDocumento = Column(String(50), nullable=False) #PDF, DOCX, XML
    versionDocumento = Column(Integer, nullable=False)
    cantPaginas = Column(Integer, nullable=False)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    firmado = Column(Boolean, default=False)
    estado = Column(Boolean, default=False) # Indica si el documento actual es la ultima version
    documentoOrigenId = Column(Integer, nullable=True)
    qrId = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True) # Borrado logico
    hashTabla = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Documento(documentoId={self.documentoId}, firmaDigitalId={self.firmaDigitalId}, cddId={self.cddId}, nombreArchivo={self.nombreArchivo}, tipoDocumento={self.tipoDocumento}, versionDocumento={self.versionDocumento}, cantPaginas={self.cantPaginas}, fechaCreacion={self.fechaCreacion}, firmado={self.firmado}, estado={self.estado}, documentoOrigenId={self.documentoOrigenId}, qrId={self.qrId}, activo={self.activo}, hashTabla={self.hashTabla})>"

    