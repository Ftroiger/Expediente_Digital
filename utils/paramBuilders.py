# param_builders.py

from datetime import datetime
from utils.hash.hashTabla import generarHash

def buildExpedienteParams(tipoExpedienteId, expedientePadreId, numeroExpediente, areaIniciadoraId,usuarioFisicoId, usuarioCreadorId, asuntoExpediente, visibilidadExpediente, temaNombre, foliosApertura, idExpedienteSirad):
    return {
        "p_tipo_expediente_id": tipoExpedienteId,
        "p_expediente_padre_id": expedientePadreId,
        "p_numero_expediente": numeroExpediente,
        "p_area_iniciadora_id": areaIniciadoraId,
        "p_usuario_fisico_id": usuarioFisicoId,
        "p_usuario_creador_id": usuarioCreadorId,
        "p_asunto_expediente": asuntoExpediente,
        "p_visibilidad_expediente": visibilidadExpediente,
        "p_activo": True,
        "p_tema_nombre": temaNombre,
        "p_folios_apertura": foliosApertura,
        "p_folios_actuales": foliosApertura,
        "p_documento_sirad_id": idExpedienteSirad
    }

def buildMovimientoParams(tramiteId, expedienteResultId, usuarioId, usuarioCreadorId, areaInicioId,areaDestinoId, observaciones):
    return {
        "p_tramite_id":  tramiteId,
        "p_expediente_id": expedienteResultId,
        "p_usuario_id":usuarioId,
        "p_usuario_origen_id": usuarioCreadorId,
        "p_area_origen_id": areaInicioId,
        "p_area_destino_id": areaDestinoId,
        "p_observacion_movimiento": observaciones,
        "p_activo": True
    }

def buildDocumentoParams(documentoCddId, nombre_archivo, tipo_documento, version, paginas, firmado):
    return {
        "p_cdd_id": documentoCddId,
        "p_nombre_archivo": nombre_archivo,
        "p_tipo_documento": tipo_documento,
        "p_version_documento": version,
        "p_cant_paginas": paginas,
        "p_firmado": firmado,
        "p_activo": True,
        "p_hash_tabla": "HASHDUMP"
    }

def buildRelacionParams(movimientoId, documentoId, foliosInicial, foliosFinal):
    return {
        "p_movimientoId": movimientoId,
        "p_documentoId": documentoId,
        "p_foliosInicial": foliosInicial,
        "p_foliosFinal": foliosFinal,
        "p_activo": True
    }

def buildHistorialEstadoParams(expedienteId, estadoId):
    return {
        "p_estadoExpedienteId": estadoId,
        "p_expedienteId": expedienteId,
        "p_fechaHasta": None,
        "p_activo": True,
        "p_hashTabla": generarHash({
            "estadoId": estadoId,
            "expedienteId": expedienteId,
            "activo": True
        })
    }

def buildPermisoParams(nombrePermiso, descripcionPermiso):
    return {
        "p_nombre_permiso": nombrePermiso,
        "p_descripcion_permiso": descripcionPermiso,
    }

def buildRolParams(nombreRol, descripcionRol):
    return {
        "p_nombre_rol": nombreRol,
        "p_descripcion_rol": descripcionRol,
    }

def buildUsuarioParams(nombreUsuario, cuilUsuario, areaId, aplicacionVediId, apiKey):
    return {
        "p_nombre_usuario": nombreUsuario,
        "p_cuil_usuario": cuilUsuario,
        "p_area_id": areaId,
        "p_aplicacion_vedi_id": aplicacionVediId,
        "p_api_key": apiKey,
        "p_activo": True 
    }

def deleteUsuarioParams(usuarioId):
    return {
        "p_usuario_id": usuarioId
    }