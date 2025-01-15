/* FUNCIONES ALMACENADAS PARA EL HISTORIAL DE ESTADO DE EXPEDIENTE */

CREATE OR REPLACE FUNCTION public."crearHistorialEstadoExpediente"(
    p_estado_expediente_id INT,
    p_expediente_id INT,
    p_fecha_hasta TIMESTAMP,
    p_activo BOOLEAN,
    p_hash_tabla VARCHAR(100)
)RETURNS TABLE(
    historial_estado_expediente_id INT,
    estado_expediente_id INT,
    expediente_id INT,
    fecha_desde TIMESTAMP,
    fecha_hasta TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE 
    temp_historial_estado_expediente_id INT;
    temp_fecha_desde TIMESTAMP;
BEGIN
    IF EXISTS(
        SELECT 1
        FROM "HistorialEstadoExpediente"
        WHERE expediente_id = p_expediente_id
    )THEN
    RETURN QUERY SELECT
        historial_estado_expediente_id AS historialEstadoExpedienteId,
        estado_expediente_id AS estadoExpedienteId,
        expediente_id AS expedienteId,
        fecha_desde,
        fecha_hasta,
        activo,
        hash_tabla AS hashTabla;
    ELSE
    INSERT INTO "HistorialEstadoExpediente"(
        "estadoExpedienteId", "expedienteId", "fechaHasta", "activo", "hashTabla"
    ) VALUES(
        p_estado_expediente_id, p_expediente_id, p_fecha_hasta, p_activo, p_hash_tabla
    )
    RETURNING "historialEstadoExpedienteId", "fechaDesde" INTO temp_historial_estado_expediente_id, temp_fecha_desde;

    RETURN QUERY SELECT
        temp_historial_estado_expediente_id AS historialEstadoExpedienteId,
        p_estado_expediente_id AS estadoExpedienteId,
        p_expediente_id AS expedienteId,
        temp_fecha_desde AS fechaDesde,
        p_fecha_hasta AS fechaHasta,
        p_activo AS activo,
        p_hash_tabla AS hashTabla;
    END IF;
END;
$$;

/* Funcion que se va a utilizar en flujo creacion de movimiento para verificar la existencia y el estado de un estaodExpedienteId*/
CREATE OR REPLACE FUNCTION public."obtenerEstadoExpedienteIdporExpedienteId"(
    p_numero_expediente VARCHAR(50)
) RETURNS TABLE(
    estado_expediente_id INT,
    nombre_estado_expediente VARCHAR(50),
    descripcion_estado_expediente VARCHAR(100),
    activo BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT e."estadoExpedienteId", e."nombreEstadoExpediente", e."descripcionEstadoExpediente", e."activo"
    FROM "EstadoExpediente" e
    JOIN "HistorialEstadoExpediente" h ON h."estadoExpedienteId" = e."estadoExpedienteId"
    JOIN "Expediente" ex ON ex."expedienteId" = h."expedienteId"
    WHERE ex."numeroExpediente" = p_numero_expediente
    -- ORDER BY h."historialEstadoExpedienteId" DESC
    LIMIT 1;

    -- Si no se encuentra un resultado, se genera un error
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe un estado activo para este expediente';
    END IF;
END;
$$;
