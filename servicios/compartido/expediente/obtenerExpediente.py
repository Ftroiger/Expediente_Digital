from db.databaseUtils import realizarConexionBD
from db.models.expediente import Expediente
from servicios.hash.verificarHash import verificarHash
from utils.error.errors import ErrorResponse, ServiceException
from schemes.expedienteScheme import ExpedienteResponse

# Función que obtiene un expediente por su número de expediente
async def obtenerExpedientePorNumeroExpediente(expedienteNumero, db) -> ExpedienteResponse: 
    """
    Parámetros:
        - expedienteNumero: str

    Retorna:
        - ExpedienteResponse

    Excepciones:
        - ServiceException(404, "No se encuentra el expediente solicitado", extra={"numeroExpediente": expedienteNumero})
        - ServiceException(404, "El expediente solicitado se encuentra inactivo", extra={"numeroExpediente": expedienteNumero})
        - ServiceException(500, "Error al obtener el expediente", extra={"error": str(e), "numeroExpediente": expedienteNumero})
    """
    try:
        # Se crea un diccionario con los parámetros necesarios para la consulta
        params = {
            "p_numeroExpediente": expedienteNumero
        }
        # Obtener el expediente
        expedienteResultList = await realizarConexionBD(procNombre="obtenerExpedientePorNumeroExpediente", procParams=params, db=db, model=ExpedienteResponse)
        expedienteResult = expedienteResultList["rows"][0]

        # Verificación del hash
        if not verificarHash(expedienteResult, Expediente, expedienteResult.hashTabla):
            raise ServiceException(status_code=500, detail="El hash del expediente no coincide", extra={"numeroExpediente": expedienteNumero})

        return expedienteResult
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        if "No existe el expediente con el numero de" in str(e):
            raise ServiceException(status_code=404, detail="No se encuentra el expediente solicitado", extra={"numeroExpediente": expedienteNumero})
        elif "El expediente se encuentra inactivo" in str(e):
            raise ServiceException(status_code=404, detail="El expediente solicitado se encuentra inactivo", extra={"numeroExpediente": expedienteNumero})
        else:
            raise ServiceException(status_code=500, detail="Error al obtener el expediente", extra={"error": str(e), "numeroExpediente": expedienteNumero})


# Función que obtiene todos los expedientes
async def obtenerExpedientes(db, skip=0, limit=10) -> list[ExpedienteResponse]: 
    """
    Parámetros:
        - db: Session

    Retorna:
        - list[ExpedienteResponse]

    Excepciones:
        - ServiceException(500, "Error al obtener los expedientes", extra={"error": str(e)})
    """
    try:
        params = {
            "p_skip": skip,
            "p_limit": limit
        }

        # Obtener los expedientes
        expedientesResultList = await realizarConexionBD(procNombre="obtenerExpedientes", procParams=params, db=db, model=ExpedienteResponse)
        expedientesResult = expedientesResultList["rows"]
        # Verificación del hash
        for expediente in expedientesResult:
            if not verificarHash(expediente, Expediente, expediente.hashTabla):
                raise ServiceException(status_code=500, detail="El hash del expediente no coincide", extra={"numeroExpediente": expediente.numeroExpediente})

        return expedientesResult
    
    
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al obtener los expedientes", extra={"error": str(e)})