from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Query
from typing import List
from schemes.estadoExpedienteScheme import estadoExpedienteCreate, estadoExpedienteResponse, estadoExpedienteUpdate
from db.models.estadoExpediente import EstadoExpediente
from db.database import get_db
from utils.hash.hashTabla import generarHash  
from utils.error.errors import ErrorResponse
from utils.responses import generate_response
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger("Expediente")

router = APIRouter()

@router.post("",
            response_model=estadoExpedienteResponse,
            tags=["Estado Expediente"], 
            summary="Crear nuevo estadoExpediente", 
            description="Crea un nuevo estadoExpediente en la base de datos",
            responses=generate_response("post", schema=estadoExpedienteResponse),)
def createEstadoExpediente(estadoExp: estadoExpedienteCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si existe un estado con el mismo nombre o descripción
        estadoExistente = db.query(EstadoExpediente).filter(
            (EstadoExpediente.nombreEstadoExpediente == estadoExp.nombreEstadoExpediente) |
            (EstadoExpediente.descripcionEstadoExpediente == estadoExp.descripcionEstadoExpediente)
        ).first()
        
        if estadoExistente:
            return ErrorResponse(status_code=400, detail="Estado con el mismo nombre o descripción ya existe.")
        
        # Preparar los datos para generar el hash
        dataParaHash = {
            "nombreEstadoExpediente": estadoExp.nombreEstadoExpediente,
            "descripcionEstadoExpediente": estadoExp.descripcionEstadoExpediente,
            "activo": estadoExp.activo,
        }
        hashGenerado = generarHash(dataParaHash)
        
        # Crear el objeto estadoExpediente
        newEstadoExpediente = EstadoExpediente(
            nombreEstadoExpediente=estadoExp.nombreEstadoExpediente,
            descripcionEstadoExpediente=estadoExp.descripcionEstadoExpediente,
            activo=estadoExp.activo,
            hashTabla=hashGenerado
        )
        
        # Agregar y confirmar la nueva entrada en la base de datos
        db.add(newEstadoExpediente)
        db.commit()
        db.refresh(newEstadoExpediente)
        
        logger.debug("Estado de expediente creado exitosamente", extra={"estadoExpedienteId": newEstadoExpediente.estadoExpedienteId})
        return newEstadoExpediente
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error de base de datos: %s", str(e))
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        logger.error("HTTP Exception: %s", str(e))
        return e
    except Exception as exc:
        logger.error(f"Exception: {str(exc)}")
        return ErrorResponse(status_code=500, detail="Error al crear estado de expediente")
    
@router.get("",
            response_model=List[estadoExpedienteResponse],
            tags=["Estado Expediente"], 
            summary="Obtener lista de estadoExpediente", 
            description="Obtiene una lista de estadoExpediente en la base de datos",
            responses=generate_response("get_all", schema=estadoExpedienteResponse, column="estadoExpediente"),)
def getEstadosExpediente(db: Session = Depends(get_db)):
    try:
        # Realizar la consulta a la base de datos
        logger.debug("Obteniendo lista de estado de expediente")
        return db.query(EstadoExpediente).all()
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error de base de datos: %s", str(e))
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        logger.error("HTTP Exception: %s", str(e))
        return e
    except Exception as exc:
        logger.error(f"Exception: {str(exc)}")
        return ErrorResponse(status_code=500, detail="Error al traer la lista de estado de expediente")
    
@router.get("/{estadoExpedienteId}",
            response_model=estadoExpedienteResponse,
            tags=["Estado Expediente"], 
            summary="Obtener un estadoExpediente", 
            description="Obtiene un estadoExpediente especifico por su ID",
            responses=generate_response("get_one", schema=estadoExpedienteResponse, column="estadoExpediente"),)
def getEstadoExpediente(estadoExpedienteId: int, db: Session = Depends(get_db)):
    try:
        estadoExpediente = db.query(EstadoExpediente).filter(EstadoExpediente.estadoExpedienteId == estadoExpedienteId).first()
        
        if not estadoExpediente:
            return ErrorResponse(status_code=404, detail="Estado de expediente no encontrado")
        logger.debug("Estado de expediente encontrado", extra={"estadoExpedienteId": estadoExpediente.estadoExpedienteId})
        return estadoExpediente
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error de base de datos: %s", str(e))
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        logger.error("HTTP Exception: %s", str(e))
        return e
    except Exception as exc:
        logger.error(f"Exception: {str(exc)}")
        return ErrorResponse(status_code=500, detail="Error al traer el estado de expediente")
    
@router.put("/{estadoExpedienteId}",
            response_model=estadoExpedienteResponse,
            tags=["Estado Expediente"], 
            summary="Actualizar estadoExpediente", 
            description="Actualiza un estadoExpediente por su ID",
            responses=generate_response("put", schema=estadoExpedienteResponse),)
def updateEstadoExpediente(estadoExpedienteId: int, estadoExp: estadoExpedienteUpdate, db: Session = Depends(get_db)):
    try:
        # Verificar si existe el estado de expediente
        estadoExpediente = db.query(EstadoExpediente).filter(EstadoExpediente.estadoExpedienteId == estadoExpedienteId).first()
        
        if not estadoExpediente:
            return ErrorResponse(status_code=404, detail="Estado de expediente no encontrado")
        
        # Actualizar solo los campos que se han modificado
        if estadoExp.nombreEstadoExpediente is not None:
            estadoExpediente.nombreEstadoExpediente = estadoExp.nombreEstadoExpediente
        if estadoExp.descripcionEstadoExpediente is not None:
            estadoExpediente.descripcionEstadoExpediente = estadoExp.descripcionEstadoExpediente
        if estadoExp.activo is not None:
            estadoExpediente.activo = estadoExp.activo
        
        # Preparar los datos para generar el hash
        dataParaHash = {
            "nombreEstadoExpediente": estadoExpediente.nombreEstadoExpediente,
            "descripcionEstadoExpediente": estadoExpediente.descripcionEstadoExpediente,
            "activo": estadoExpediente.activo,
        }
        hashGenerado = generarHash(dataParaHash)
        estadoExpediente.hashTabla = hashGenerado
        
        # Confirmar la actualización en la base de datos
        db.commit()
        db.refresh(estadoExpediente)
        
        logger.debug("Estado de expediente actualizado", extra={"estadoExpedienteId": estadoExpediente.estadoExpedienteId})
        return estadoExpediente
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error de base de datos: %s", str(e))
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        logger.error("HTTP Exception: %s", str(e))
        return e
    except Exception as exc:
        logger.error(f"Exception: {str(exc)}")
        return ErrorResponse(status_code=500, detail="Error al actualizar estado de expediente")
    
@router.delete("/{estadoExpedienteId}",
               response_model=estadoExpedienteResponse,
               tags=["Estado Expediente"], 
               summary="Eliminar un estadoExpediente", 
               description="Elimina un estadoExpediente por su ID",
               responses=generate_response("delete"),)
def deleteEstadoExpediente(estadoExpedienteId: int, db: Session = Depends(get_db)):
    try:
        # Verificar si existe el estado de expediente
        estadoExpediente = db.query(EstadoExpediente).filter(EstadoExpediente.estadoExpedienteId == estadoExpedienteId).first()
        
        if not estadoExpediente:
            return ErrorResponse(status_code=404, detail="Estado de expediente no encontrado")
        
        # Marcar el estado de expediente como inactivo
        estadoExpediente.activo = False

        # Actualizar el Hash
        dataParaHash = {
            "nombreEstadoExpediente": estadoExpediente.nombreEstadoExpediente,
            "descripcionEstadoExpediente": estadoExpediente.descripcionEstadoExpediente,
            "activo": estadoExpediente.activo,
        }
        hashGenerado = generarHash(dataParaHash)
        estadoExpediente.hashTabla = hashGenerado

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(estadoExpediente)
        logger.debug("Estado de expediente eliminado", extra={"estadoExpedienteId": estadoExpediente.estadoExpedienteId})
        return estadoExpediente
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error de base de datos: %s", str(e))
        return ErrorResponse(status_code=500, detail="Error en la base de datos", extra={"error": str(e)})
    except ErrorResponse as e:
        logger.error("HTTP Exception: %s", str(e))
        return e
    except Exception as exc:
        logger.error(f"Exception: {str(exc)}")
        return ErrorResponse(status_code=500, detail="Error al eliminar estado de expediente")
