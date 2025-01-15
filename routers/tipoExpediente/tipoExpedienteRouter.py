import logging
from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.database import get_db
from db.models.tipoExpediente import TipoExpediente
from db.databaseUtils import getConnection
from routers import tipoExpediente
from schemes.tipoExpedienteScheme import ActualizarTipoExpediente,  TipoExpedienteCreate, TipoExpedienteResponse
from utils.error.errors import ErrorResponse
from utils.hash.hashTabla import generarHash
from utils.log.logging_config import logger
from utils.responses import generate_response


logger = logging.getLogger("Expediente")

router = APIRouter()\


@router.post("",
            response_model=TipoExpedienteResponse,
            summary="Crear nuevo tipo de expediente",
            description="Crea un nuevo tipo de expediente en la base de datos",
            tags=["Tipo Expediente"],
            responses=generate_response("post", schema=TipoExpedienteResponse))
def create_tipoexpediente(tipoexpediente: TipoExpedienteCreate, db: Session = Depends(get_db)):
    
    try:
        
        # Preparar los datos para generar el hash
        data_para_hash = {
            "nombreTipoExpediente": tipoExpediente.nombreTipoExpediente,
            "descripcionTipoExpediente": tipoExpediente.descripcionTipoExpediente,
            "activo": tipoExpediente.activo
        }
        
        # Generar el hash en los datos clave del modelo
        hash_generado = generarHash(data_para_hash)
        
        # Crear el objeto `TipoExpediente` con el hash generado
        db_tipoexpediente = TipoExpediente(
            nombreTipoExpediente=tipoExpediente.nombreTipoExpediente,
            descripcionTipoExpediente=tipoExpediente.descripcionTipoExpediente,
            activo=tipoExpediente.activo,
            hashTabla=hash_generado
        )
        db.add(db_tipoexpediente)
        db.commit()
        db.refresh(db_tipoexpediente)
        logger.debug(f"Se creo nuevo tipo de expediente")
        return db_tipoexpediente

    except SQLAlchemyError as e:
        db.rollback()
        # Extraemos el detalle del error y lo almacenamos en una variable
        error_detail = str(e.orig).split("DETAIL:")[1].strip()  # Ajusta esto según la estructura de tu error
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": error_detail})

@router.get("/{tipoexpediente_id}",
            response_model=TipoExpedienteResponse,
            summary="Obtener tipo de expediente por ID",
            description="Obtiene un tipo de expediente específico por su ID",
            tags=["Tipo Expediente"],
            responses=generate_response("get_one", schema=TipoExpedienteResponse, column="tipoExpediente"))
def get_tipoexpediente(tipoexpediente_id: int, db: Session = Depends(get_db)):
    try:
        # Validar que el ID del tipo de expediente sea positivo
        if tipoexpediente_id <= 0:
            return ErrorResponse(status_code=400, detail="El ID del tipo de expediente debe ser un número positivo")

        db_tipoexpediente = db.query(TipoExpediente).filter(TipoExpediente.tipoExpedienteId == tipoexpediente_id).first()
        
        if db_tipoexpediente is None:
            return ErrorResponse(status_code=404, detail="TipoExpediente no encontrado")
        logger.debug(f"Se obtuvo tipo de expediente con id: {tipoexpediente_id}")
        return db_tipoexpediente

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        return e
    except Exception as exc:
        return ErrorResponse(status_code=500, detail="Error al trae un tipo de expediente")

@router.get("",
            response_model=List[TipoExpedienteResponse],
            summary="Obtener todos los tipos de expediente",
            description="Obtiene una lista de todos los tipos de expediente",
            tags=["Tipo Expediente"],
            responses=generate_response("get_all", schema=TipoExpedienteResponse, column="tipoExpediente"))
async def get_tipoexpedientes(db: Session = Depends(get_db)):
    try:
        # Conexión a la base de datos
        result = await getConnection("obtenerTipoExpedientes",None, db,keep=True)
        if isinstance(result, ErrorResponse):
            return result
        
        tipoExpedientes = result["rows"]
        if not tipoExpedientes:
            return ErrorResponse(status_code=404, detail="No se encontraron tipos de expediente")
        logger.debug(f"Se obtuvo lista de tipos de expediente")
        return tipoExpedientes
    
    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        return e
    except Exception as exc:
        return ErrorResponse(status_code=500, detail="Error al traer una lista de tipos de expediente")

@router.put("/{tipoexpediente_id}",
            response_model=TipoExpedienteResponse,
            summary="Actualizar tipo de expediente",
            description="Actualiza un tipo de expediente existente por su ID",
            tags=["Tipo Expediente"],
            responses=generate_response("put", schema=TipoExpedienteResponse))
def update_tipoexpediente(tipoexpediente_id: int, tipoexpediente: TipoExpedienteCreate, db: Session = Depends(get_db)):
    try:
        # Validar que el ID del tipo de expediente sea positivo
        if tipoexpediente_id <= 0:
            return ErrorResponse(status_code=400, detail="El ID del tipo de expediente debe ser un número positivo")

        db_tipoexpediente = db.query(TipoExpediente).filter(TipoExpediente.tipoExpedienteId == tipoexpediente_id).first()
        
        if db_tipoexpediente is None:
            return ErrorResponse(status_code=404, detail="TipoExpediente no encontrado")
        
        for key, value in tipoexpediente.dict().items():
            setattr(db_tipoexpediente, key, value)

        # Preparar los datos para generar el hash
        data_para_hash = {
            "tipoExpedienteId": db_tipoexpediente.tipoExpedienteId,
            "nombreTipoExpediente": db_tipoexpediente.nombreTipoExpediente,
            "descripcionTipoExpediente": db_tipoexpediente.descripcionTipoExpediente,
            "activo": db_tipoexpediente.activo
        }

        # Generar el hash en los datos clave del modelo
        hash_generado = generarHash(data_para_hash)
        db_tipoexpediente.hashTabla = hash_generado
        
        db.commit()
        db.refresh(db_tipoexpediente)

        logger.debug(f"Se actualizo tipo de expediente con id: {tipoexpediente_id}")
        return db_tipoexpediente

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        return e
    except Exception as exc:
        return ErrorResponse(status_code=500, detail="Error al actualizar un tipo de expediente")

@router.delete("/{tipoexpediente_id}", 
               response_model=TipoExpedienteResponse,
               summary="Eliminar tipo de expediente", 
               description="Elimina un tipo de expediente existente",
               tags=["Tipo Expediente"],
               responses=generate_response("delete"))
def delete_tipoexpediente(tipoexpediente_id: int, db: Session = Depends(get_db)):
    try:
        db_tipoexpediente = db.query(TipoExpediente).filter(TipoExpediente.tipoExpedienteId == tipoexpediente_id).first()
        if db_tipoexpediente is None:
            return ErrorResponse(status_code=404, detail="TipoExpediente no encontrado")
        db.delete(db_tipoexpediente)
        db.commit()
        logger.debug(f"Se elimino tipo de expediente con id: {tipoexpediente_id}")
        return {"message": "TipoExpediente eliminado"}
    
    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        return e
    except Exception as exc:
        return ErrorResponse(status_code=500, detail="Error al eliminar un tipo de expediente")
