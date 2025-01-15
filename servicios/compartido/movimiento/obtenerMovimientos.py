from db.databaseUtils import realizarConexionBD
from schemes.movimientoScheme import MovimientoResponse
from db.models.movimiento import Movimiento
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ServiceException
from typing import List

# Función que obtiene todos los movimientos relacionados a un expediente
async def obtenerMovimientosPorExpedienteId(expedienteId: int, db) -> List[MovimientoResponse]:
    try:
        # Crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_expedienteId": expedienteId
        }
        # Obtener los movimientos por expediente
        movimientos = await realizarConexionBD("obtenerMovimientosPorExpedienteId", params, db, model=MovimientoResponse, keep=True)
        # Verificación del hash
        for movimiento in movimientos["rows"]:
            if not verificarHash(movimiento, Movimiento, movimiento.hashTabla):
                raise ServiceException(500, "El hash del movimiento no coincide", extra={"movimientoId": movimiento.movimientoId})
        
        return movimientos["rows"]
    
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al obtener los movimientos del expediente", extra={"error": str(e)})
    
async def obtenerMovimientos(db)->list[MovimientoResponse]:
    try:
        movimientos = await realizarConexionBD("obtenerMovimientos", {}, db, model=MovimientoResponse, keep=True)
        for movimiento in movimientos["rows"]:
            if not verificarHash(movimiento, Movimiento, movimiento.hashTabla):
                raise ServiceException(500, "El hash del movimiento no coincide", extra={"movimientoId": movimiento.movimientoId})
        return movimientos["rows"]
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al obtener los movimientos", extra={"error": str(e)})