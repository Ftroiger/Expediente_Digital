from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func,Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.movimiento import Movimiento
from db.models.documento import Documento


class DocumentoXMovimiento(Base):
    __tablename__ = 'DocumentoXMovimiento'
    __table_args__ = {'extend_existing': True}

    documentoXMovimientoId =Column(Integer,primary_key=True)
    movimientoId = Column(Integer,ForeignKey('Movimiento.movimientoId'),nullable=False) 
    documentoId = Column(Integer,ForeignKey('Documento.documentoId'),nullable=False) 
    fechaAsociacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    foliosInicial = Column(Integer,nullable=True)
    foliosFinal = Column(Integer,nullable=True)
    activo = Column(Boolean,nullable=False,default=True)
    hashTabla = Column(String(100),nullable=False)

    movimiento = relationship('Movimiento')
    documento = relationship('Documento')

    @classmethod
    def crearRelacion(cls, session, movimientoId, documentoId, foliosInicial, foliosFinal, hashTabla):
        """
        Crea una relación entre un documento y un movimiento.

        Parámetros:
            - session: Session -> Sesión de la base de datos.
            - movimientoId: int -> ID del movimiento.
            - documentoId: int -> ID del documento.
            - foliosInicial: int -> Folio inicial del documento.
            - foliosFinal: int -> Folio final del documento.

        Retorna:
            - bool -> True si la relación fue creada exitosamente, False en caso contrario.
        """
        try:
            relacion = cls(movimientoId=movimientoId, documentoId=documentoId, foliosInicial=foliosInicial, foliosFinal=foliosFinal, hashTabla=hashTabla)
            session.add(relacion)
            return True
        except Exception as e:
            return False