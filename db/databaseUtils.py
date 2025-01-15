from typing import List, Any, Dict, Optional, Type
from sqlalchemy import text
from db.database import get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.error.errors import ServiceException
from typing import Any, List, Dict
from utils.error.errors import ServiceException
import os


# Llamar procedimiento almacenado para insertar registro
async def insertConnection(procNombre: str, procParams: dict, db: Session, keep: bool = False):
    """
    Parámetros:
    - procNombre: Nombre del procedimiento almacenado a ejecutar
    - procParams: Parámetros del procedimiento almacenado en forma de dict = {param1: valor1, param2: valor2, ...}
    - db: Conexión a la base de datos

    Retorno:
    - Diccionario con el resultado de la consulta = {columna1: valor1, columna2: valor2, ...}

    """
    if db is None:
        raise ServiceException(status_code=500, detail="Error al conectar a la base de datos", extra={"procedimiento": procNombre})
    
    try:
        if procParams:
            # Llamar la db funcion con los parametros pasados
            query = (
                f"""SELECT * FROM public."{procNombre}"(:{', :'.join(procParams.keys())})"""
            )
            result = db.execute(text(query), procParams)
        else:
            # Llamar la db funcion sin parametros
            query = (
                f"SELECT * FROM public.{procNombre}()"
            )
            result = db.execute(text(query))
                
        # Obtener el resultado de la consulta
        rows = result.fetchall()
        columns_snake = result.keys()

        # Convertir los nombres de las columnas de snake_case a camelCase
        columns = snakeToCamel(columns_snake)

        if not rows:
            raise ServiceException(status_code=500, detail="No se encontraron resultados", extra={"procedimiento": procNombre})

        # Convertir el resultado a un diccionario
        rowsDict = [resultToDict(row, columns) for row in rows]
        return rowsDict
      
    
    except Exception as e:
        raise e

    finally:
        if not keep:
            db.close()


# Llamar un procedimiento almacenado para obtener registros
async def getConnection(
        procNombre: str, 
        procParams: dict, 
        db: Session,
        model: Optional[Type[BaseModel]] = None,
        keep: bool = False):
    """
    Parámetros:
        - procNombre: Nombre del procedimiento almacenado a ejecutar
        - procParams: Parámetros del procedimiento almacenado en forma de dict = {param1: valor1, param2: valor2, ...}
        - db: Conexión a la base de datos
        - model: Modelo de Pydantic para convertir el resultado a un objeto
        - keep: Mantener la conexión abierta después de ejecutar el procedimiento almacenado

    Retorno:
        - Diccionario con el resultado de la consulta = {
                "rows": [objeto1, objeto2, ...],
            }
    """
    if db is None:
        raise ServiceException(status_code=500, detail="Error al conectar a la base de datos", extra={"procedimiento": procNombre})
    
    try:
        if procParams:
            # Llamar la db funcion con los parametros pasados
            query = (
                f"""SELECT * FROM public."{procNombre}"(:{', :'.join(procParams.keys())})"""
            )
            result = db.execute(text(query), procParams)
        else:
            # Llamar la db funcion sin parametros
            query = (
                f"""SELECT * FROM public."{procNombre}"()"""
            )
            result = db.execute(text(query))
        if not keep:
            db.commit()

        # Obtener el resultado de la consulta
        rows = result.fetchall()
        columns_snake = result.keys()
        # Convertir los nombres de las columnas de snake_case a camelCase
        columns = snakeToCamel(columns_snake)
        if len(rows) > 0:
            if model:
                # Convertir el resultado a un objeto de Pydantic
                rows = [model(**resultToDict(row, columns)) for row in rows]
            else:
                # Convertir el resultado a un diccionario
                rows = [resultToDict(row, columns) for row in rows]
        else:
            rows = []
        return {
            "rows": rows,
        }
    
    # Lanzar la excepción si ocurre un error a la función que llama a esta función
    except Exception as e:
        raise e

    finally:
        if not keep:
            db.close()


# Función para llamar un procedimiento almacenado para actualizar registros
async def putConnection(procNombre: str, 
                        procParams: dict, 
                        db: Session, 
                        model: Optional[Type[BaseModel]] = None,
                        keep: bool = False):
    """
    Parámetros:
        - procNombre: Nombre del procedimiento almacenado a ejecutar
        - procParams: Parámetros del procedimiento almacenado en forma de dict = {param1: valor1, param2: valor2, ...}
        - db: Conexión a la base de datos
        - keep: Mantener la conexión abierta después de ejecutar el procedimiento almacenado

    Retorno:
        - Diccionario con el resultado de la consulta = {
                        "rows": [objeto1, objeto2, ...],
                    }
    """
    if db is None:
        raise ServiceException(status_code=500, detail="Error al conectar a la base de datos", extra={"procedimiento": procNombre})
    
    try:
        if procParams:
            # Llamar la db funcion con los parametros pasados
            query = (
                f"""SELECT * FROM public."{procNombre}"(:{', :'.join(procParams.keys())})"""
            )
            result = db.execute(text(query), procParams)
        else:
            # Llamar la db funcion sin parametros
            query = (
                f"""SELECT * FROM public."{procNombre}"()"""
            )
            result = db.execute(text(query))
        if not keep:
            db.commit()

        # Obtener el resultado de la consulta
        rows = result.fetchall()
        columns_snake = result.keys()
        # Convertir los nombres de las columnas de snake_case a camelCase
        columns = snakeToCamel(columns_snake)
        if len(rows) > 0:
            if model:
                # Convertir el resultado a un objeto de Pydantic
                rows = [model(**resultToDict(row, columns)) for row in rows]
            else:
                # Convertir el resultado a un diccionario
                rows = [resultToDict(row, columns) for row in rows]
        else:
            rows = []
        return {
            "rows": rows,
        }
    
    # Lanzar la excepción si ocurre un error a la función que llama a esta
    except Exception as e:
        raise e

    finally:
        if not keep:
            db.close()


# Función general para realizar una acción a la base de datos
async def realizarConexionBD(procNombre: str, 
                             procParams: dict,
                             db: Session,
                             model: Optional[Type[BaseModel]] = None,
                             keep: bool = False):
    """
    Función general para realizar una acción a la base de datos. Puede ser para insertar, obtener o actualizar registros.
    El tipo de conexión se determina por el procedimiento almacenado.

    Parámetros:
    - procNombre: Nombre del procedimiento almacenado a ejecutar
    - procParams: Parámetros del procedimiento almacenado en forma de dict = {param1: valor1, param2: valor2, ...}
    - db: Conexión a la base de datos
    - model: Modelo de Pydantic para convertir el resultado a un objeto
    - keep: Mantener la conexión abierta después de ejecutar el procedimiento almacenado

    Retorno:
    - Diccionario con el resultado de la consulta = {
                    "rows": [objeto1, objeto2, ...],
                }
    
    """
    if db is None:
        raise ServiceException(status_code=500, detail="Error al conectar a la base de datos", extra={"procedimiento": procNombre})
    
    try:
        if procParams:
            # Llamar la db funcion con los parametros pasados
            query = (
                # f"""SELECT * FROM public."{procNombre}"(:{', :'.join(procParams.keys())})"""
                f"""SELECT * FROM "{procNombre}"(:{', :'.join(procParams.keys())})"""
            )
            result = db.execute(text(query), procParams)
        else:
            # Llamar la db funcion sin parametros
            query = (
                # f"""SELECT * FROM public."{procNombre}"()"""
                f"""SELECT * FROM "{procNombre}"()"""
            )
            result = db.execute(text(query))
        
        # Si no se mantiene la conexión, hacer commit
        if not keep:
            db.commit()

        # Obtener el resultado de la consulta
        rows = result.fetchall()
        columns_snake = result.keys()
        # Convertir los nombres de las columnas de snake_case a camelCase
        columns = snakeToCamel(columns_snake)
        
        if len(rows) > 0:
            if model:
                # Convertir el resultado a un objeto de Pydantic
                rows = [model(**resultToDict(row, columns)) for row in rows]
            else:
                # Convertir el resultado a un diccionario
                rows = [resultToDict(row, columns) for row in rows]
        else:
            rows = []

        
        return {
            "rows": rows,
        }
    
    except ServiceException as e:
        raise e
    
    # Lanzar la excepción si ocurre un error a la función que llama a esta
    except Exception as e:
        raise e

    finally:
        if not keep:
            db.close()




def resultToDict(rows: Any, columns: List[str]) -> Dict[str, Any]:
    """
    Función para convertir el resultado de una consulta con sqlalchemy a un diccionario.

    Parámetros:
    - rows: Resultado de la consulta con sqlalchemy -> result.fetchall()
    - columns: Nombres de las columnas de la consulta -> result.keys()

    Retorno:
    - Diccionario con los resultados de la consulta = {columna1: valor1, columna2: valor2, ...}

    """
    try:
        rowDict = {}
        for index, column in enumerate(columns):
            value = rows[index]
            rowDict[column] = value
        return rowDict
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al convertir el resultado de la consulta a un diccionario", extra={"error": str(e)})
    

def snakeToCamel(snakeList: List[str]) -> List[str]:
    """
    Función para convertir una lista de strings de snake_case a camelCase.

    Parámetros:
    - snakeList: Lista de strings en snake_case = ["string_1", "string_2", ...]

    Retorno:
    - Lista de strings en camelCase = ["String1", "String2", ...]

    """
    try:
        camelList = []
        for snake in snakeList:
            camel = ''.join(word.title() for word in snake.split('_'))
            # Convertir la primera letra a minúscula
            camel = camel[0].lower() + camel[1:]
            camelList.append(camel)
        return camelList
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al convertir de snake_case a camelCase", extra={"error": str(e)})


def _read_sql_file(filename):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    # Abre el archivo con la codificacion UTF-8
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()