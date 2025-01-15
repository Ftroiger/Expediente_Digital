from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.orm import relationship
from db.database import Base

class TipoNorma(Base):
    __tablename__ = "TipoNorma"

    tipoNormaId = Column(Integer, primary_key=True, nullable=False)
    nombreTipoNorma = Column(String(50), unique=True, nullable=False)
    descripcionTipoNorma = Column(String(255), nullable=True)
    activo = Column(Boolean, nullable=False,default=True)
    hashTabla = Column(String(100), nullable=False, unique=True)

    @classmethod
    def exists(cls, session, tipoNormaId):
        return session.query(cls).filter_by(tipoNormaId=tipoNormaId).first() is not None
    