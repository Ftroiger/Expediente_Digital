from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from db.database import Base

class Norma(Base):
    __tablename__ = "Norma"

    normaId = Column(Integer, primary_key=True, nullable=False)
    tipoNormaId = Column(Integer, ForeignKey('TipoNorma.tipoNormaId'), nullable=False)
    numeroNorma = Column(String(50), unique=True, nullable=False)
    descripcionNorma = Column(String(255), nullable=True)
    fechaCreacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    normaCddId = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)
    hashTabla = Column(String(100), nullable=False, unique=True)

    tipoNorma = relationship('TipoNorma')

    @classmethod
    def exists(cls, session, normaId):
        return session.query(cls).filter_by(normaId=normaId).first() is not None