from typing import List, Dict,Any

def leerLogs(archivo_log: str) -> List[Dict[str, str]]:
    registros = []
    try:
        with open(archivo_log, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                partes = linea.split(' /-/ ')
                if len(partes) == 7:
                    registro = {
                        "ID": partes[0].replace('ID: ', '').strip(),
                        "Fecha": partes[1].replace('Fecha: ', '').strip(),
                        "Servicio": partes[2].replace('Servicio: ', '').strip(),
                        "Nivel": partes[3].replace('Nivel: ', '').strip(),
                        "Archivo": partes[4].replace('Archivo: ', '').strip(),
                        "Clase": partes[5].replace('Clase: ', '').strip(),
                        "Descripcion": partes[6].replace('Descripcion: ', '').strip()
                    }
                    registros.append(registro)
    except UnicodeDecodeError:
        # Intentar con un códec diferente si utf-8 falla
        with open(archivo_log, 'r', encoding='latin-1') as archivo:
            for linea in archivo:
                partes = linea.split(' /-/ ')
                if len(partes) == 7:
                    registro = {
                        "ID": partes[0].replace('ID: ', '').strip(),
                        "Fecha": partes[1].replace('Fecha: ', '').strip(),
                        "Servicio": partes[2].replace('Servicio: ', '').strip(),
                        "Nivel": partes[3].replace('Nivel: ', '').strip(),
                        "Archivo": partes[4].replace('Archivo: ', '').strip(),
                        "Clase": partes[5].replace('Clase: ', '').strip(),
                        "Descripcion": partes[6].replace('Descripcion: ', '').strip()
                    }
                    registros.append(registro)
    return registros

def filtrarLogs(registros: List[Dict[str, Any]], fechaDesde: str, fechaHasta: str, servicio: str, nivel: str) -> List[Dict[str, Any]]:
    resultados_filtrados = []
    for registro in registros:
        fecha_registro = registro['Fecha'].split(' ')[0]  # Extrae solo la parte de la fecha
        if (
            (not fechaDesde or fecha_registro >= fechaDesde) and
            (not fechaHasta or fecha_registro <= fechaHasta) and
            (not servicio or registro['Servicio'] == servicio) and
            (not nivel or registro['Nivel'] == nivel)
        ):
            if fechaHasta and not fechaDesde:
                if fecha_registro == fechaHasta:
                    resultados_filtrados.append(registro)
            else:
                resultados_filtrados.append(registro)
    return resultados_filtrados