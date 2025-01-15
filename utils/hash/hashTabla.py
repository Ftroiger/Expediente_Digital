import hashlib
from datetime import datetime
from utils.error.errors import ServiceException

def generarHash(data):
    """
    Genera un hash SHA-256 a partir de un objeto, respetando el formato de la cadena 1.

    Args:
        obj dict: Un diccionario con los datos del objeto.

    Returns:
        str: El hash SHA-256 generado a partir del objeto.
    """

    # Crear una instancia de hash SHA-256
    hash = hashlib.sha256()

    # Iterar sobre los elementos del diccionario ordenado por claves
    values = []
    for key in data.keys():
        if key in "hashTabla":
            continue
        value = data[key]
        if isinstance(value, datetime):
            # Convertir a cadena con formato personalizado (reemplazando T por espacio)
            value = value.strftime("%Y-%m-%d %H:%M:%S.%f")
            if value.endswith('0'):
                value = value[:-1]
        else:
            if value is True:
                # Convertir a cadena "true" si el valor es True
                value = "true"
            elif value is False:
                # Convertir a cadena "false" si el valor es False
                value = "false"
            value = str(value) if value is not None else ""
        values.append(value)


    # Unir los valores en una cadena sin espacios adicionales
    concatenatedData = "".join(values)

    # Actualizar el hash con la clave y el valor
    hash.update(concatenatedData.encode('utf-8'))

    # Devolver el hash en formato hexadecimal
    return hash.hexdigest()
