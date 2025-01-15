# Funcion que verifica que un registro se encuentre activo
from utils.error.errors import ServiceException


def verificarEstadoActivo(registros):
    try:
        registrosActivos = []
        for registro in registros:
            #Verificar si el registro es un diccionario
            if isinstance(registro, dict):
                #Verificar el valor de la propiedad activo
                if registro.get('activo', True):
                    registrosActivos.append(registro)

            # Verificar si el registro es un objeto
            elif hasattr(registro, 'activo'):
                # Verificar el valor de la propiedad activo
                if registro.activo :
                    registrosActivos.append(registro)
        
        return registrosActivos

    except Exception as e:
        raise ServiceException(status_code=500, detail="Error al verificar estado del registro", extra={"error": str(e), "activo": registros['activo']})
    