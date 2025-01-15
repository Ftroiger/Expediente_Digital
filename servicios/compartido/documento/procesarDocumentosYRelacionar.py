from sqlalchemy.orm import Session
from servicios.cdd.cdd import cargarYConfirmarDocumentoEnCDD
from servicios.compartido.documento.insertarDocumentoBdd import insertarDocumentoBdd
from servicios.compartido.documento.crearRelacionDocumentoMovimiento import crearRelacionDocumentoMovimiento
import logging
from utils.error.errors import ServiceException

async def procesarDocumentoYRelacionar(
    documentoInfo: dict,
    movimientoId: int,
    db: Session,
    cuilOperador: str,
    cuilPropietario: str
):
    try:
        # Cargar y confirmar el documento en el CDD
        docCddId = await cargarYConfirmarDocumentoEnCDD(
            {
                "nombreArchivo": documentoInfo["nombre"],
                "DocumentBytes": documentoInfo["contenido"]
            },
            cuilOperador=cuilOperador,
            cuilPropietario=cuilPropietario
        )

        # Insertar el documento en la base de datos usando insertarDocumentoBdd
        documentoResult = await insertarDocumentoBdd(docCddId,documentoInfo["nombre"],"IPJ - Formulario C", 1, documentoInfo["cantidadPaginas"], documentoInfo["firmado"] or False, db)
    
        # Crear la relación entre el documento y el movimiento usando crearRelacionDocumentoMovimiento
        relacionResult = await crearRelacionDocumentoMovimiento(
            movimientoId,
            documentoResult.documentoId,
            documentoInfo.get("folioInicial"),
            documentoInfo.get("folioFinal"),
            db
        )

        # Retornar el resultado de la relación
        return relacionResult
    except ServiceException as e:
        raise e
    except Exception as e:
        raise ServiceException(500, "Error al procesar el documento y relacionarlo con el movimiento", extra={"message": str(e)})