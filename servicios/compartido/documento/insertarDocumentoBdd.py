from db.models.documento import Documento
from utils.error.errors import ServiceException
from db.databaseUtils import realizarConexionBD
from sqlalchemy.orm import Session

from utils.paramBuilders import buildDocumentoParams

async def insertarDocumentoBdd(documentoCddId,nombre_archivo,tipo_documento, version, paginas, firmado, db: Session):
    """
    Inserts a new document into the database.

    This function attempts to create a new document entry in the database using the provided
    parameters. If successful, it returns the created document. If a document with the same
    name already exists, or if there's an error during insertion, it raises appropriate exceptions.

    Args:
        documentoCddId (str): The unique identifier for the document in CDD.
        nombre_archivo (str): The name of the document file.
        tipo_documento (str): The type of the document.
        version (str): The version of the document.
        paginas (int): The number of pages in the document.
        db (Session): The database session object.

    Returns:
        dict: The first element of the list returned by the database insertion operation,
            which represents the created document.
    """
    try:
        documentoCddId
        params = buildDocumentoParams(
        documentoCddId,
        nombre_archivo,
        tipo_documento,
        version,
        paginas,
        firmado
        )
        documentoResultDict = await realizarConexionBD("crearDocumento", params, db, keep=True, model=Documento)

        documentoResult = documentoResultDict["rows"][0]

        return documentoResult
    
    except ServiceException as e:
        raise e

    except Exception as e:
        if f"Ya existe un documento esta referencia a cdd" in str(e):
            raise ServiceException(404, "Ya existe un documento en CDD con ese cddId", extra={"nombre_archivo": nombre_archivo})
        else:
            raise ServiceException(500, "Error al insertar documento en CDD", extra={"error": str(e), "nombre_archivo": nombre_archivo})