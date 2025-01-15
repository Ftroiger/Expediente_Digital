CREATE OR REPLACE FUNCTION "calcularHashSha256"(texto TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN encode(digest(texto, 'sha256'), 'hex');
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "calcularHashPermiso"
(
    p_permiso_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    permiso_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    SELECT 
        COALESCE("permisoId"::TEXT, '') || 
        COALESCE("nombrePermiso"::TEXT, '') ||
        COALESCE("descripcionPermiso"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO permiso_data
    FROM "Permiso"
    WHERE "permisoId" = p_permiso_id;

    IF permiso_data IS NULL THEN
        RAISE EXCEPTION 'Permiso con ID % no encontrado', p_permiso_id;
    END IF;

    hash_result := "calcularHashSha256"(permiso_data);

    RETURN hash_result;
END;
$$;


CREATE OR REPLACE FUNCTION "calcularHashMovimiento"
(
    p_movimiento_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    movimiento_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del movimiento en un único texto
    SELECT 
        COALESCE("movimientoId"::TEXT, '') ||
        COALESCE("tramiteId"::TEXT, '') ||
        COALESCE("expedienteId"::TEXT, '') ||
        COALESCE("usuarioFisicoId"::TEXT, '') ||
        COALESCE("usuarioAplicacionId"::TEXT, '') ||
        COALESCE("areaOrigenId"::TEXT, '') ||
        COALESCE("areaDestinoId"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("observacionMovimiento"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO movimiento_data
    FROM "Movimiento"
    WHERE "movimientoId" = p_movimiento_id;

    -- Si no se encuentra el movimiento, lanzar un error
    IF movimiento_data IS NULL THEN
        RAISE EXCEPTION 'Movimiento con ID % no encontrado', p_movimiento_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(movimiento_data);

    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashHistorialEstadoExpediente"
(
    p_historial_estado_expediente_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    historial_estado_expediente_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del historial de estado expediente en un único texto
    SELECT 
        COALESCE("historialEstadoExpedienteId"::TEXT, '') || 
        COALESCE("estadoExpedienteId"::TEXT, '') ||
        COALESCE("expedienteId"::TEXT, '') ||
        COALESCE("fechaDesde"::TEXT, '') ||
        COALESCE("fechaHasta"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO historial_estado_expediente_data
    FROM "HistorialEstadoExpediente"
    WHERE "historialEstadoExpedienteId" = p_historial_estado_expediente_id;

    -- Si no se encuentra el historial de estado expediente, lanzar un error
    IF historial_estado_expediente_data IS NULL THEN
        RAISE EXCEPTION 'Historial de estado expediente con ID % no encontrado', p_historial_estado_expediente_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(historial_estado_expediente_data);

    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashExpediente"(
    p_expediente_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    expediente_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del expediente en un único texto
    SELECT 
        COALESCE("expedienteId"::TEXT, '') || 
        COALESCE("tipoExpedienteId"::TEXT, '') ||
        COALESCE("expedientePadreId"::TEXT, '') ||
        COALESCE("numeroExpediente"::TEXT, '') ||
        COALESCE("areaIniciadoraId"::TEXT, '') ||
        COALESCE("usuarioCreadorFisicoId"::TEXT, '') ||
        COALESCE("usuarioCreadorAplicacionId"::TEXT, '') ||
        COALESCE("asuntoExpediente"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("fechaUltimoMovimiento"::TEXT, '') ||
        COALESCE("visibilidadExpediente"::TEXT, '') ||
        COALESCE("activo"::TEXT, '') ||
        COALESCE("temaNombre"::TEXT, '') ||
        COALESCE("areaActualidadId"::TEXT, '') ||
        COALESCE("foliosApertura"::TEXT, '') ||
        COALESCE("foliosActuales"::TEXT, '') ||
        COALESCE("documentoSiradId"::TEXT, '')
    INTO expediente_data
    FROM "Expediente"
    WHERE "expedienteId" = p_expediente_id;

    -- Si no se encuentra el expediente, lanzar un error
    IF expediente_data IS NULL THEN
        RAISE EXCEPTION 'Expediente con ID % no encontrado', p_expediente_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(expediente_data);

    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashRol"
(
    p_rol_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    rol_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    SELECT 
        COALESCE("rolId"::TEXT, '') || 
        COALESCE("nombreRol"::TEXT, '') ||
        COALESCE("descripcionRol"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO rol_data
    FROM "Rol"
    WHERE "rolId" = p_rol_id;

    IF rol_data IS NULL THEN
        RAISE EXCEPTION 'Rol con ID % no encontrado', p_rol_id;
    END IF;

    hash_result := "calcularHashSha256"(rol_data);

    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashRolXPermiso"
(
    p_rol_x_permiso_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    rol_x_permiso_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    SELECT 
        COALESCE("rolXPermisoId"::TEXT, '') || 
        COALESCE("permisoId"::TEXT, '') ||
        COALESCE("rolId"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO rol_x_permiso_data
    FROM "RolXPermiso"
    WHERE "rolXPermisoId" = p_rol_x_permiso_id;

    IF rol_x_permiso_data IS NULL THEN
        RAISE EXCEPTION 'Rol x permiso con ID % no encontrado', p_rol_x_permiso_id;
    END IF;

    hash_result := "calcularHashSha256"(rol_x_permiso_data);

    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashDocumentoXMovimiento"
(   
    p_documento_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    documento_x_movimiento_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del documento x movimiento en un único texto
    SELECT 
        COALESCE("documentoXMovimientoId"::TEXT, '') || 
        COALESCE("movimientoId"::TEXT, '') ||
        COALESCE("documentoId"::TEXT, '') ||
        COALESCE("fechaAsociacion"::TEXT, '') ||
        COALESCE("foliosInicial"::TEXT, '') ||
        COALESCE("foliosFinal"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO documento_x_movimiento_data
    FROM "DocumentoXMovimiento"
    WHERE "documentoId" = p_documento_id;

    -- Si no se encuentra el documento x movimiento, lanzar un error
    IF documento_x_movimiento_data IS NULL THEN
        RAISE EXCEPTION 'Documento x movimiento con ID % no encontrado', p_documento_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(documento_x_movimiento_data);

    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashDocumento"
(
    p_documento_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    documento_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del documento en un único texto
    SELECT 
        COALESCE("documentoId"::TEXT, '') || 
        COALESCE("firmaDigitalId"::TEXT, '') ||
        COALESCE("cddId"::TEXT, '') ||
        COALESCE("nombreArchivo"::TEXT, '') ||
        COALESCE("tipoDocumento"::TEXT, '') ||
        COALESCE("versionDocumento"::TEXT, '') ||
        COALESCE("cantPaginas"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("firmado"::TEXT, '') ||
        COALESCE("estado"::TEXT, '') ||
        COALESCE("documentoOrigenId"::TEXT, '') ||
        COALESCE("qrId"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO documento_data
    FROM "Documento"
    WHERE "documentoId" = p_documento_id;

    -- Si no se encuentra el documento, lanzar un error
    IF documento_data IS NULL THEN
        RAISE EXCEPTION 'Documento con ID % no encontrado', p_documento_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(documento_data);

    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashUsuario"
(
    p_usuario_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    usuario_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del usuario en un único texto
    SELECT 
        COALESCE("usuarioId"::TEXT,'') ||
        COALESCE("cuilUsuario"::TEXT,'') ||
        COALESCE("nombreUsuario"::TEXT,'') ||
        COALESCE("fechaCreacion"::TEXT,'') ||
        COALESCE("fechaBaja"::TEXT,'') ||
        COALESCE("areaId"::TEXT,'') ||
        COALESCE("aplicacionVediId"::TEXT,'') ||
        COALESCE("apiKey"::TEXT,'') ||
        COALESCE("usuarioAlta"::TEXT,'') ||
        COALESCE("activo"::TEXT,'')
    INTO usuario_data
    FROM "Usuario"
    WHERE "usuarioId" = p_usuario_id;

    -- Si no se encuentra el usuario, lanzar un error
    IF usuario_data IS NULL THEN
        RAISE EXCEPTION 'Usuario con ID % no encontrado', p_usuario_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(usuario_data);
    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashRolXUsuario"
(
    p_rol_x_usuario_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    rol_x_usuario_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del rol por usuario en un único texto
    SELECT 
        COALESCE("rolXUsuarioId"::TEXT,'') ||
        COALESCE("usuarioId"::TEXT,'') ||
        COALESCE("rolId"::TEXT,'') ||
        COALESCE("fechaCreacion"::TEXT,'') ||
        COALESCE("activo"::TEXT,'')
    INTO rol_x_usuario_data
    FROM "RolXUsuario"
    WHERE "rolXUsuarioId" = p_rol_x_usuario_id;

    -- Si no se encuentra el movimiento, lanzar un error
    IF rol_x_usuario_data IS NULL THEN
        RAISE EXCEPTION 'Movimiento con ID % no encontrado', p_rol_x_usuario_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(rol_x_usuario_data);

    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashRolXPermiso"
(
    p_rol_x_permiso_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    rol_x_permiso_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del rol por permiso en un único texto
    SELECT 
        COALESCE("rolXPermisoId"::TEXT,'') ||
        COALESCE("permisoId"::TEXT,'') ||
        COALESCE("rolId"::TEXT,'') ||
        COALESCE("fechaCreacion"::TEXT,'') ||
        COALESCE("activo"::TEXT,'')
    INTO rol_x_permiso_data
    FROM "RolXPermiso"
    WHERE "rolXPermisoId" = p_rol_x_permiso_id;

    -- Si no se encuentra el movimiento, lanzar un error
    IF rol_x_permiso_data IS NULL THEN
        RAISE EXCEPTION 'Rol por permiso con ID % no encontrado', p_rol_x_permiso_id;
    END IF;

    -- Calcular el hash utilizando la función calcularHashSha256
    hash_result := "calcularHashSha256"(rol_x_permiso_data);

    -- Retornar el hash calculado
    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashNotificacion"(
    p_notificacion_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    notificacion_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos de la notificación en un único texto
    SELECT
        COALESCE("notificacionId"::TEXT, '') ||
        COALESCE("usuarioNotificadoId"::TEXT, '') ||
        COALESCE("tipoNotificacionId"::TEXT, '') ||
        COALESCE("descripcionNotificacion"::TEXT, '') ||
        COALESCE("usuarioAfectadoId"::TEXT, '') ||
        COALESCE("leido"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO notificacion_data
    FROM "Notificacion"
    WHERE "notificacionId" = p_notificacion_id;

    IF notificacion_data IS NULL THEN
        RAISE EXCEPTION 'Notificación con ID % no encontrada', p_notificacion_id;
    END IF;

    hash_result := "calcularHashSha256"(notificacion_data);

    RETURN hash_result;
END;
$$;

CREATE OR REPLACE FUNCTION "calcularHashTipoNotificacion"(
    p_tipo_notificacion_id INTEGER
)
RETURNS VARCHAR(100)
LANGUAGE plpgsql
AS $$
DECLARE
    tipo_notificacion_data TEXT;
    hash_result VARCHAR(100);
BEGIN
    -- Concatenar todos los atributos del tipo de notificación en un único texto
    SELECT
        COALESCE("tipoNotificacionId"::TEXT, '') ||
        COALESCE("nombreTipoNotificacion"::TEXT, '') ||
        COALESCE("descripcionTipoNotificacion"::TEXT, '') ||
        COALESCE("fechaCreacion"::TEXT, '') ||
        COALESCE("activo"::TEXT, '')
    INTO tipo_notificacion_data
    FROM "TipoNotificacion"
    WHERE "tipoNotificacionId" = p_tipo_notificacion_id;

    IF tipo_notificacion_data IS NULL THEN
        RAISE EXCEPTION 'Tipo de notificación con ID % no encontrado', p_tipo_notificacion_id;
    END IF;

    hash_result := "calcularHashSha256"(tipo_notificacion_data);

    RETURN hash_result;
END;
$$;


