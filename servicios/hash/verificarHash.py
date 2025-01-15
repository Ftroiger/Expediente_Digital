from sqlalchemy import inspect

from utils.error.errors import ServiceException
from utils.hash.hashTabla import generarHash

# Función para verificar el hash de un objeto
def verificarHash(objeto, modeloDb, hashObjeto):
    """
    Parámetros:
        - objeto: objeto
        - modeloDb: modelo de la base de datos sqlalchemy

    Retorna:
        - bool

    Excepciones:
        - 
    """
    try:
        # ---- NORMALIZAR OBJETO (para incluir campos requeridos y excluir campos no deseados)
        # Obtener los campos requeridos del modelo
        camposRequeridos = [columna.name for columna in inspect(modeloDb).c]

        # Normalizar el objeto
        objetoDict = objeto.__dict__
        objetoNormalizado = {k: v for k, v in objetoDict.items() if k in camposRequeridos}

        # ---- OBTENER HASH
        # Obtener el hash del objeto
        hashGenerado = generarHash(objetoNormalizado)
        
        # Comparar los hashes
        if hashGenerado == hashObjeto:
            return True
        else:
            return False

    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al verificar el hash del objeto", extra={"error": str(e)})