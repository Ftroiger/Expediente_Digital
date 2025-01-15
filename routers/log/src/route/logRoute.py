import logging
import os
from fastapi import APIRouter, Query
import math

from routers.log.src.logUtils import filtrarLogs, leerLogs
from utils.error.errors import ErrorResponse

logger = logging.getLogger("Expediente")
logger.setLevel(logging.DEBUG)

router = APIRouter()

@router.get("/logs")
def obtenerLogs(
    fechaDesde: str = Query(None),
    fechaHasta: str = Query(None),
    servicio: str = Query(None),
    nivel: str = Query(None),
    pag: int = Query(1, gt=0),
    limite: int = Query(10, gt=0)  # Cambié el valor por defecto a 10 para más claridad
):
    """Endpoint para obtener los logs filtrados."""
    archivo_log = 'expediente.log'  # Ajusta la ruta si es necesario

    # Verificar si el archivo de logs existe
    if not os.path.exists(archivo_log):
        return ErrorResponse(status_code=404, detail="El archivo de logs no existe.")

    try:
        logger.debug("Llamada a obtener_logs")
        registros = leerLogs(archivo_log)
        resultados = filtrarLogs(registros, fechaDesde, fechaHasta, servicio, nivel)

        # Calcular la cantidad total de páginas
        totalRegistros = len(resultados)
        paginasTotales = math.ceil(totalRegistros / limite)

        # Paginación
        indexInicial = (pag - 1) * limite
        finIndex = indexInicial + limite
        resultadosPaginados = resultados[indexInicial:finIndex]

        return {"logs": resultadosPaginados, "totalPaginas": paginasTotales}

    except Exception as e:
        logger.error(f"Error al obtener los logs: {str(e)}")
        return {"error": str(e)}
