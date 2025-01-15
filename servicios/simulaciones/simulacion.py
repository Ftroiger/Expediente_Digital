from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Image
import os
from utils.error.errors import ServiceException
import io
import re
import qrcode
from servicios.baseUnica.apiBaseUnica import getDependenciaById
from servicios.sirad.sirad import consultarTemas


async def generarCaratula(numeroExpediente, asuntoExpediente, temaExpediente, fechaCreacion, areaIniciadoraId):
    """
    Genera una carátula en formato PDF para el expediente con los datos proporcionados y la guarda en Downloads.

    Parámetros:
        numeroExpediente: str -> Número del expediente.
        asuntoExpediente: str -> Asunto del expediente.
        fechaCreacion: str -> Fecha de creación del expediente.
        areaIniciadoraId: int -> ID del área iniciadora.

    Retorna:
        dict: Contiene 'Error', 'DocumentBytes', 'DocumentName', 'DocumentExtension', 'DocumentMimeType'
    """
    # Validar que ninguno de los parámetros requeridos sea None o vacío
    if not numeroExpediente:
        raise ServiceException(400, "El número del expediente es obligatorio para la carátula.")

    if not asuntoExpediente:
        raise ServiceException(400, "El asunto del expediente es obligatorio para la carátula.")

    if not temaExpediente:
        raise ServiceException(400, "El tema del expediente es obligatorio para la carátula.")

    if not fechaCreacion:
        raise ServiceException(400, "La fecha de creación del expediente es obligatoria para la carátula.")

    if not areaIniciadoraId:
        raise ServiceException(400, "El ID del área iniciadora es obligatorio para la carátula.")
    
    # Validar que el tema proporcionado exista
    tema_valido = await validarTema(temaExpediente)
    if not tema_valido:
        raise ServiceException(400, f"El tema '{temaExpediente}' no es válido o no existe en la lista de temas disponibles.")

    try:
        buffer = io.BytesIO()

        # Configurar el documento con márgenes estrechos
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm
        )
        elements = []

        # Estilos personalizados
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        # Estilo para el título central
        styleTitle = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=26,
            leading=22,
            spaceAfter=12
        )

        # Estilo para textos en negrita
        styleBold = ParagraphStyle(
            'Bold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=14
        )

        styleBoldUnderline = ParagraphStyle(
            'BoldUnderline',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=20,
        )

        # Estilo para textos normales
        styleNormal = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=12,
            leading=14
        )

        # Estilo para textos centrados
        styleCenter = ParagraphStyle(
            'Center',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            fontSize=12,
            leading=14
        )

        # Estilo para el número de expediente
        styleNumeroExpediente = ParagraphStyle(
            'NumeroExpediente',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            fontSize=17,
            leading=20
        )

        # Estilo para la fecha en rojo
        styleRed = ParagraphStyle(
            'Red',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            textColor=colors.red,
            fontSize=12,
            leading=14
        )

        styleFieldLarge = ParagraphStyle(
            'FieldLarge',
            parent=styles['Normal'],
            fontSize=20,  # Ajusta el tamaño de fuente aquí
            leading=20
        )

        # Estilos para etiquetas y valores en la última sección
        styleLabel = ParagraphStyle(
            'Label',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=16,
            underlineProportion=0.1
        )

        styleValue = ParagraphStyle(
            'Value',
            parent=styles['Normal'],
            fontSize=14,
            leading=16
        )
        # ---------- Encabezado Superior Derecho ----------
        # Cuadro "Reservado para archivo" con divisiones y alineado a la derecha
        reservado_para_archivo = Table(
            [
                [Paragraph("Reservado Para Archivo", styleCenter)],
                [Paragraph("Nº de Orden", styleCenter)],
                [""]  # Fila en blanco para la línea de división
            ],
            colWidths=[50 * mm],
            rowHeights=[8 * mm, 8 * mm, 7 * mm]  # Ajuste de altura en la fila inferior para más espacio
        )

        reservado_para_archivo.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),  # Línea divisoria después de la segunda fila
            ('BOTTOMPADDING', (0, 0), (0, 0), 2),  # Reducir el espacio después del primer renglón
        ]))

        # Crear una tabla de una sola celda para alinear el cuadro a la derecha
        tabla_derecha = Table([[reservado_para_archivo]], colWidths=[None, 50 * mm])

        # Alineación derecha del cuadro
        tabla_derecha.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ]))

        # Añadir a `elements` para que quede alineado a la derecha
        elements.append(tabla_derecha)

        # ---------- Escudo y Título Central ----------

        # Añadir logo
        logo = Image("LogoMunicipalidad.png", width=20 * mm, height=30 * mm)
        elements.append(logo)
        elements.append(Spacer(1, 10 * mm))
        elements.append(Paragraph("<b>MUNICIPALIDAD DE CÓRDOBA</b>", styleTitle))
        elements.append(Spacer(1, 5 * mm))

        # ---------- Sección de Identificación del Expediente ----------
        numero_expediente = str(numeroExpediente)
        fecha_actual = fechaCreacion.strftime("%d/%m/%Y")

        # Área iniciadora (puedes ajustar esto según tus datos)
        # area_iniciadora = str(areaIniciadoraId)
        dependenciaData = await getDependenciaById(areaIniciadoraId)
        area_iniciadora = dependenciaData[0]["unidad"]
        altura_total_recuadro = 58 * mm

        # Recuadro izquierdo
        recuadro_izquierdo_contenido = Table(
            [
                [Paragraph("<b>Expediente Nº</b>", styleBold)],
                [Paragraph(f"<b>{numero_expediente}</b>", styleNumeroExpediente)]
            ],
            colWidths=[85 * mm],
            rowHeights=[10 * mm, altura_total_recuadro - 10 * mm]
        )

        recuadro_izquierdo_contenido.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        recuadro_izquierdo = Table([[recuadro_izquierdo_contenido]], colWidths=[85 * mm], rowHeights=[altura_total_recuadro])
        recuadro_izquierdo.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Recuadro derecho
        recuadro_derecho_contenido = Table(
            [
                [Paragraph("<b>MUNICIPALIDAD DE<br/>CÓRDOBA</b>", styleCenter)],
                [Spacer(1, 5 * mm)],
                [Table(  # Recuadro interno con la fecha
                    [
                        [Paragraph(f"<font color='red'><b>{fecha_actual}</b></font>", styleRed)]
                    ],
                    colWidths=[40 * mm],
                    rowHeights=[10 * mm],
                    style=TableStyle([
                        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Recuadro alrededor de la fecha
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),       # Centrar la fecha
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                    ])
                )],
                [Spacer(1, 5 * mm)],
                [Paragraph("<b>DIRECCIÓN GENERAL DE<br/>ATENCIÓN AL VECINO</b>", styleCenter)]
            ],
            colWidths=[85 * mm],
            rowHeights=[12 * mm, 5 * mm, 20 * mm, 5 * mm, 16 * mm]
        )

        recuadro_derecho_contenido.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        recuadro_derecho = Table([[recuadro_derecho_contenido]], colWidths=[85 * mm], rowHeights=[altura_total_recuadro])
        recuadro_derecho.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Tabla que contiene los recuadros izquierdo y derecho
        identificacion_expediente = Table(
            [
                [recuadro_izquierdo, recuadro_derecho]
            ],
            colWidths=[85 * mm, 85 * mm],
            rowHeights=[altura_total_recuadro]
        )
        identificacion_expediente.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))

        # Añadir a los elementos
        elements.append(identificacion_expediente)
        elements.append(Spacer(1, 10 * mm))

        # ---------- Información del Iniciador, Asunto y Tema ----------
        iniciador = str(area_iniciadora)
        asunto = str(asuntoExpediente)
        tema = str(temaExpediente)

        # Agrgar validación del tema que envia el vertical haciendo un get temas y verificando que exista


        elementos_info = [
            [Paragraph("Iniciador:", styleLabel), Paragraph(iniciador, styleValue)],
            [Paragraph("Asunto:", styleLabel), Paragraph(asunto, styleValue)],
            [Paragraph("Tema:", styleLabel), Paragraph(tema, styleValue)],
        ]

        row_heights = [15 * mm, 15 * mm, 15 * mm]

        tabla_info = Table(elementos_info, colWidths=[40 * mm, 120 * mm], rowHeights=row_heights)
        tabla_info.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(tabla_info)
        elements.append(Spacer(1, 10 * mm))

        # ---------- Generar y Agregar Código QR ----------
        # Llamar a la función que genera el código QR
        qr_code_bytes = generarCodigoQR(numeroExpediente)

        # Crear un objeto Image de ReportLab directamente desde los bytes
        qr_image_obj = Image(io.BytesIO(qr_code_bytes), width=30 * mm, height=30 * mm)

        # Añadir el QR al elemento
        elements.append(qr_image_obj)
        elements.append(Spacer(1, 10 * mm))

        # Construir el documento
        doc.build(elements)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        expediente_num = re.sub(r'[<>:"/\\|?*]', '_', numero_expediente)
        filename = f"Caratula_Expediente_{expediente_num}.pdf"

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        with open(downloads_path, "wb") as f:
            f.write(pdf_bytes)

        respuesta = {
            "Error": "",
            "DocumentBytes": pdf_bytes,
            "DocumentName": filename,
            "DocumentExtension": "pdf",
            "DocumentMimeType": "application/pdf",
            "FilePath": downloads_path
        }
        return respuesta

    except Exception as e:
        raise ServiceException(500, "Error al generar la carátula del expediente", extra={"message": str(e)})

def calcularPesoDocumento(documento):
    """
    Calcula el tamaño en bytes de un documento en formato PDF.

    Parámetros:
        documento: dict -> Diccionario que contiene los bytes del documento bajo la clave "DocumentBytes".

    Retorna:
        int -> Tamaño en bytes del documento.
    """
    return len(documento["DocumentBytes"])

def generarCodigoQR(numeroExpediente):
    """
    Genera un código QR con la URL del indice de un Expediente

    Parámetros: numeroExpediente: str -> Número del expediente.

    Retorna: bytes -> Contenido de la imagen del código QR.
    """    

    # Construir la URL
    url = f"http://localhost:3000/expedientes/detalle/{numeroExpediente}"
    
    # Generar el código QR
    qr_img = qrcode.make(url)

    # Guardar la imagen en bytes
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    # Retornar los bytes de la imagen
    return buffer.getvalue()

async def validarTema(nombreTema):
    """
    Valida si el nombreTema existe en la lista de temas obtenida de SIRAD.

    Args:
        nombreTema (str): El nombre del tema a validar.

    Returns:
        bool: True si el tema existe, False en caso contrario.
    """
    try:
        temas = await consultarTemas()
        # Suponiendo que cada tema es un diccionario con la clave 'nombre'
        return any(tema.get('Nombre') == nombreTema for tema in temas)
    except Exception as e:
        # Puedes manejar la excepción según tus necesidades
        raise e
    
