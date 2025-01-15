from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func, Boolean
from db.database import Base
from sqlalchemy.orm import Session

class TipoExpediente(Base):
    __tablename__ = "TipoExpediente"

    tipoExpedienteId = Column(Integer, primary_key=True)
    nombreTipoExpediente = Column(String(50), unique=True, nullable=False)
    descripcionTipoExpediente = Column(String(255))

    activo = Column(Boolean, nullable=False ,default=True) 
    hashTabla = Column(String(100), nullable=False, unique=True)


    @classmethod
    def obtenerTipoExpediente(cls, session: Session, nombreTipoExpediente: str):
        """
        Busca el tipo de expediente por su nombre.

        Parámetros:
            - session: Session -> Sesión de la base de datos.
            - nombreTipoExpediente: str -> Nombre del tipo de expediente.

        Retorna:
            - Optional[int] -> ID del tipo de expediente. Si no se encuentra, retorna None.
        """
        try:
            tipoExpediente = session.query(cls).filter(cls.nombreTipoExpediente == nombreTipoExpediente).first()
            if tipoExpediente:
                return tipoExpediente.tipoExpedienteId
            return None
        except Exception as e:
            return None