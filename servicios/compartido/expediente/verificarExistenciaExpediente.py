from db.databaseUtils import realizarConexionBD
from utils.error.errors import ServiceException

# Función para verificar la existencia de un expediente por número
async def verificarExistenciaExpedientePorNumero(numeroExpediente: str, db) -> bool:
    """
    Verifica si existe un expediente con el número proporcionado en la base de datos.

    Parámetros:
        - numeroExpediente (str): El número de expediente a verificar.
        - db: Conexión a la base de datos.

    Retorna:
        - True si el expediente existe.
        - False si el expediente no existe.
        - ErrorResponse en caso de error.
    """
    try:
        # Llamar a la función almacenada en la base de datos
        resultado = await realizarConexionBD(
            "verificarExistenciaNumeroExpediente",
            {"p_numero_expediente": numeroExpediente},
            db,
            model=None,
            keep=True
        )

        # Acceder a los 'rows' del resultado
        rows = resultado.get("rows", [])

        # Verificar si hay datos en 'rows'
        if not rows:
            raise ServiceException(
                status_code=500,
                detail="Error al verificar la existencia del expediente",
                extra={"numero_expediente": numeroExpediente}
            )

        # Obtener el valor de 'existe'
        existe = rows[0]['existe']

        # Retornar el resultado
        return existe
    
    except ServiceException as e:
        raise e

    except Exception as e:
        raise ServiceException(
            status_code=500,
            detail="Error al verificar la existencia del expediente",
            extra={"error": str(e), "numero_expediente": numeroExpediente}
        )
