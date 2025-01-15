import io
from docx import Document
from PyPDF2 import PdfReader

from utils.error.errors import ServiceException

# Función para contar el número de páginas de un documento DOCX
def contarPaginasDOCX(contenidoDocumento):
    """
    Función para contar el número de páginas de un documento DOCX.

    Parámetros:
        contenidoDocumento: bytes

    Retorno:
        int = Número de páginas del documento
    """
    # Crear documento DOCX
    doc = Document(io.BytesIO(contenidoDocumento))

    # Contar páginas
    return len(doc.element.xpath('//w:sectPr'))

# Función para contar el número de páginas de un documento PDF
def contarPaginasPDF(contenidoDocumento):
    """
    Función para contar el número de páginas de un documento PDF.

    Parámetros:
        contenidoDocumento: bytes

    Retorno:
        int = Número de páginas del documento
    """
    # Crear documento PDF
    pdfStream = io.BytesIO(contenidoDocumento)

    # Contar páginas
    pdf = PdfReader(pdfStream)

    # Si se encuentra encriptado, retornar -1
    if pdf.is_encrypted:
        return 0
    
    return len(pdf.pages)


# Función general para contar el número de páginas de un documento
def contarPaginasDocumento(contenidoDocumento, tipoDocumento):
    """
    Función para contar el número de páginas de un documento.

    Parámetros:
        contenidoDocumento: bytes
        tipoDocumento: str

    Retorno:
        int = Número de páginas del documento
    """
    if tipoDocumento == "DOCX":
        return contarPaginasDOCX(contenidoDocumento)
    elif tipoDocumento == "PDF":
        return contarPaginasPDF(contenidoDocumento)
    else:
        return -1
    

# Función para detectar si el pdf contiene una firma digital
def contieneFirmaDigitalPDF(contenidoDocumento):
    """
    Función para detectar si un documento PDF contiene una firma digital.

    Parámetros:
        contenidoDocumento: bytes

    Retorno:
        bool = True si el documento contiene una firma digital, False en caso contrario
    """
    try:
        pdf = PdfReader(contenidoDocumento)

        if pdf.is_encrypted:
            return False

        root = pdf.trailer["/Root"]

        # Fijar en 'Perms'
        perms = root.get("/Perms")
        if perms:
            perms = perms.get_object()  # Resolver objeto indirecto
            if '/DocMDP' in perms or '/UR' in perms or '/UR3' in perms:
                return True  # Certificado o reader enabled

        # Fijar en 'AcroForm'
        acroForm = root.get("/AcroForm")
        if acroForm:
            acroForm = acroForm.get_object()  # Resolver objeto indirecto

            # Fijar en 'XFA'
            if '/XFA' in acroForm:
                return False

            # Fijar en 'SigFlags'
            if '/SigFlags' in acroForm and acroForm['/SigFlags'] > 0:
                return True

            # Fijar en 'Fields'
            fields = acroForm.get('/Fields', [])
            for field in fields:
                field_resolved = field.get_object()  # Resolver objeto indirecto
                if field_resolved.get('/FT') == '/Sig' and field_resolved.get('/V') is not None:
                    return True

        return False
    
    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al intentar detectar firma digital en PDF. Es probable que el archivo esté encriptado", extra={"error": str(e)})

    