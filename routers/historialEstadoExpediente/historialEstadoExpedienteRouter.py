from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Query
from typing import List
from schemes.historialEstadoExpedienteScheme import HistorialEstadoExpedienteResponse
from db.models.historialEstadoExpediente import HistorialEstadoExpediente
from db.database import get_db
from utils.error.errors import ErrorResponse
import logging

logger = logging.getLogger("Expediente")

router = APIRouter()

#Mock de la base de datos
todos={}

@router.get("/filter", response_model=List[HistorialEstadoExpedienteResponse])
def getHistorialEstadoExpedienteByFilter(
    expedienteId: int = Query(None, description="ID del expediente"),
    estadoId: int = Query(None, description="ID del estado"),
    pagina: int = Query(1, ge=1, description="Número de página, debe ser mayor a 1"),
    cantidadFilas: int = Query(10, ge=1, le=100, description="Número de filas por página, debe ser entre 1 y 100"),
    db: Session = Depends(get_db)
):
    try:
        # Paginación y consulta
        logger.debug(f"Consulta de historial de estado de expediente con filtro")
        return db.query(HistorialEstadoExpediente).all()
    
    except SQLAlchemyError as e:
        return ErrorResponse(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        return ErrorResponse(status_code=500, detail="Error interno del servidor")
    

from fastapi.testclient import TestClient



client = TestClient(router)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
