from io import BytesIO
from typing import List

from fastapi import File, UploadFile
from utils.documentoTools import contarPaginasDocumento, contieneFirmaDigitalPDF
from utils.error.errors import ErrorResponse, ServiceException

async def procesarFoliajeDocumentos(folioApertura, files: List[UploadFile] = File(...)):
    """
    Función para procesar y preparar los archivos para el foliaje de los documentos.

    Parámetros:
        archivos: list = [
            Files
        ],
        folioApertura: int

    Retorno:
        list = [
            {
                "nombreArchivo": str,
                "extension": str,
                "contenido": str,
                "peso": str,
                "cantidadPaginas": int,
                "folioInicial": int,
                "folioFinal": int
            }
        ]

    """
    try:
        archivosInfo = []
        folioActual = folioApertura

        for file in files:
            # Verificar la extensión
            if file.content_type not in ["application/pdf"]:
                raise ServiceException(status_code=400, detail="El archivo subido no es un PDF", extra={"archivo": file.filename})
            
            # Extraer contenido
            contenido = await file.read()

            # Verificar firma digital sin consumir el contenido
            # Create a new BytesIO object from the file content to preserve it for other operations
            contenido_stream = BytesIO(contenido)
            firmado = contieneFirmaDigitalPDF(contenido_stream)

            # Extraer peso
            peso = len(contenido)

            # Si el peso del archivo es mayor a 10MB, retornar un error
            if peso > 10485760:
                raise ServiceException(status_code=400, detail="El archivo supera los 10MB. Disminuya el tamaño del archivo y vuelva a intentarlo", extra={"archivo": file.filename})
            
            # Contar páginas
            cantPaginas = contarPaginasDocumento(contenido, "PDF")

            # Si el número de páginas es -1, retornar un error
            if cantPaginas == -1:
                raise ServiceException(status_code=400, detail="Error al contar el número de páginas del documento", extra={"archivo": file.filename})

            # Agregar información a la lista
            archivosInfo.append({
                "nombre": file.filename,
                "extension": file.filename.split(".")[-1],
                "contenido": contenido,
                "peso": peso,
                "cantidadPaginas": cantPaginas,
                "folioInicial": folioActual+1,
                "folioFinal": folioActual+cantPaginas,
                "firmado": firmado
            })

            # Actualizar el folio actual
            folioActual += cantPaginas


        return archivosInfo
    
    except ServiceException as e:
        raise e
    
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al procesar los archivos", extra={"error": str(e)})

        
