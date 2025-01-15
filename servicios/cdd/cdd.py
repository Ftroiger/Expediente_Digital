import json
from utils.error.errors import ServiceException
from servicios.simulaciones.simulacion import calcularPesoDocumento
import httpx
import os

CDD_API_CLIENT_ID = os.getenv('CDD_API_CLIENT_ID')
CDD_API_KEY = os.getenv('CDD_API_KEY')

async def integracionDocumentosCDD(nombre, idTipoDocumento, idTipoArchivo, peso, cuilOperador, cuilPropietario=None, vencimiento=None, customId=None):
    """
    Inicia la carga de documentos en CDD y devuelve la respuesta.

    Parámetros:
        nombre: str -> Nombre completo del archivo incluyendo la extensión.
        idTipoDocumento: int -> ID del tipo de documento a cargar.
        idTipoArchivo: int -> ID del tipo de archivo a cargar.
        peso: int -> Peso del archivo en bytes.
        cuilOperador: str -> CUIL del operador que realiza la carga.
        cuilPropietario: str / None -> CUIL o CUIT del propietario del documento (opcional).
        vencimiento: str / None -> Fecha de vencimiento en formato 'YYYY-MM-DD'.
        customId: str / None -> Identificador personalizado.

    Retorna:
        dict -> Respuesta de la API de CDD.
    """
    url = "https://api.cdd.stage.cordoba.gob.ar/core-cdd-api/integracion/documentos"

    headers = {
        "x-api-client-id": CDD_API_CLIENT_ID,
        "x-api-key": CDD_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "nombre": nombre,
        "peso": peso,
        "idTipoDocumento": idTipoDocumento,
        "idTipoArchivo": idTipoArchivo,
        "cuilOperador": cuilOperador,
    }

    # Debo eliminar los guiones del cuil operador
    body["cuilOperador"] = body["cuilOperador"].replace("-", "")

    # Agregar parámetros opcionales si se proporcionan
    if cuilPropietario:
        cuilPropietarioLimpio = cuilPropietario.replace("-", "")
        if len(cuilPropietarioLimpio) == 11:
            if cuilPropietarioLimpio.startswith(('20', '23', '24', '27')):
                body["cuilPropietario"] = cuilPropietarioLimpio
            else:
                body["cuitPropietario"] = cuilPropietarioLimpio
        else:
            raise ValueError("cuilPropietario debe ser un número de 11 dígitos válido.")
    if vencimiento:
        body["vencimiento"] = vencimiento
    if customId:
        body["customId"] = customId

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=body, headers=headers)
        
        if response.status_code in [200, 201, 202, 203, 204]:
            return response.json()

        else:
            raise ServiceException(500, "Error en la integración con CDD", extra={"message": response.text})
        
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error en la integración con CDD", extra={"message": str(e)})


async def cargarYConfirmarDocumentoEnCDD(documento, cuilOperador, cuilPropietario):
    """
    Carga un documento en el sistema CDD y confirma su carga.

    Parámetros:
        documento: dict -> Información del documento, incluyendo nombre y datos en bytes.
        cuilOperador: str -> CUIL del usuario que realiza la carga.
        cuilPropietario: str / None -> CUIL o CUIT del propietario del documento (opcional).
        
    Retorna:
        int -> ID del documento en CDD si la carga y confirmación son exitosas.
    """
    try:
        # Paso 1: Solicitar URL prefirmada y otros datos del CDD
        respuestaDocumentoCDD = await integracionDocumentosCDD(
            nombre=documento["nombreArchivo"],
            idTipoDocumento=4,  # Debes reemplazar con el ID correcto
            idTipoArchivo=2,    # Debes reemplazar con el ID correcto
            peso=len(documento["DocumentBytes"]),
            cuilOperador=cuilOperador,
            cuilPropietario=cuilPropietario
        )
        
        # Extraer datos necesarios de la respuesta
        urlPrefirmada = respuestaDocumentoCDD["data"]["parts"][0]["signedUrl"]
        uploadId = respuestaDocumentoCDD["data"]["uploadId"]
        idDocumento = respuestaDocumentoCDD["data"]["idDocumento"]

        # Paso 2: Cargar el documento en la URL prefirmada
        await cargarDocumentoUrl(urlPrefirmada, documento["DocumentBytes"])

        # Paso 3: Confirmar la carga del documento en el CDD
        await confirmarCargaDocumento(uploadId, idDocumento, cuilOperador)
        # Retornar el ID del documento si todo fue exitoso
        return idDocumento
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al cargar y confirmar el documento en CDD", extra={"error": str(e)})
    
async def cargarDocumentoUrl(url, documento_bytes):
    """
    Carga el documento en la URL prefirmada.

    Parámetros:
        url: str -> URL prefirmada donde se cargará el documento.
        documento_bytes: bytes -> Contenido del documento en formato binario.
    """
    headers = {
        "Content-Type": "application/octet-stream"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, data=documento_bytes, headers=headers)
        
        if response.status_code in [200, 204]:
            return True
        else:
            raise ServiceException(500, "Error al cargar el documento en la URL prefirmada", extra={"message": response.text})

    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al cargar el documento en la URL prefirmada", extra={"message": str(e)})

async def confirmarCargaDocumento(upload_id, id_documento, cuil_operador):
    """
    Confirma que el documento ha sido cargado correctamente.

    Parámetros:
        upload_id: str -> ID de la carga obtenida de la respuesta anterior.
        id_documento: str -> ID del documento obtenido de la respuesta anterior.
        cuil_operador: str -> CUIL del operador que realiza la confirmación.
    """
    url = f"https://api.cdd.stage.cordoba.gob.ar/core-cdd-api/integracion/documentos/{id_documento}/{upload_id}/completar"

    headers = {
        "x-api-client-id": CDD_API_CLIENT_ID,
        "x-api-key": CDD_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "cuilOperador": cuil_operador
    }

    try:
        body["cuilOperador"] = body["cuilOperador"].replace("-", "")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=body, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise ServiceException(500, "Error al confirmar la carga del documento", extra={"message": response.text})
        
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al confirmar la carga del documento", extra={"message": str(e)})



# Función para obtener un documento por ID
async def obtenerDocumentoPorCddId(documentoCddId: str):
    """
    Petición a CDD para obtener un documento por ID.

    Parámetros:
        documentoId: str -> ID del documento a obtener.

    Retorna:
        dict -> Datos del documento: {
            "status": int,
            "data": {
                "nombre": str,
                "peso": int,
                "url": str
                "cuilPropietario": str,
                "cuitPropietario": str,
                "idDocumento": int,
                "tipoDocumento": int,
                "aplicacion": str,
                "customId": int,
                "fechaCreacion": str,
                "fechaActualizacion": str
            },
            "success": bool
            "message": str
        }
    """
    url = f"https://api.cdd.stage.cordoba.gob.ar/core-cdd-api/integracion/documentos/{documentoCddId}"


    headers = {
        "x-api-client-id": CDD_API_CLIENT_ID,
        "x-api-key": CDD_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise ServiceException(500, "Error al obtener el documento de CDD", extra={"message": response.text})
        
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al obtener el documento de CDD", extra={"message": str(e)})
    

# Función para obtener todos los documentos de cdd
async def obtenerDocumentosCdd():
    """
    Petición a CDD para obtener todos los documentos.

    Retorna:
        dict -> Lista de documentos: {
    """
    url = "https://api.cdd.stage.cordoba.gob.ar/core-cdd-api/integracion/documentos?offset=0&limit=50"

    headers = {
        "x-api-client-id": CDD_API_CLIENT_ID,
        "x-api-key": CDD_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise ServiceException(500, "Error al obtener los documentos de CDD", extra={"message": response.text})
        
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al obtener los documentos de CDD", extra={"message": str(e)})
