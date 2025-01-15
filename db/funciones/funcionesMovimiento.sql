CREATE OR REPLACE FUNCTION public."crearMovimiento"(
    p_tramite_id INT,
    p_expediente_id INT,
    p_usuario_fisico_id INT,
    p_usuario_aplicacion_id INT,
    p_area_origen_id INT,
    p_area_destino_id INT,
    p_observacion_movimiento TEXT,
    p_activo BOOLEAN
)
RETURNS TABLE(
    movimiento_id INT,
    tramite_id INT,
    expediente_id INT,
    usuario_fisico_id INT,
    usuario_aplicacion_id INT,
    area_origen_id INT,
    area_destino_id INT,
    fecha_creacion TIMESTAMP,
    observacion_movimiento TEXT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)LANGUAGE plpgsql
AS $$
DECLARE
    temp_movimientoId INT;
    temp_fecha_creacion TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
BEGIN

    IF NOT EXISTS( 
        SELECT 1
        FROM "Expediente"
        WHERE "expedienteId" = p_expediente_id
    ) THEN
        RAISE EXCEPTION 'El expediente no existe %', p_expediente_id;
    END IF;
    -- Verificar si ya existe un movimiento con el mismo tramiteId y expedienteId
    --ACA ESTA MAL LA VERIFICACION, SI PUEDEN EXISTIR 2 MOVIMIENTOS CON EL MISMO
    --TRAMITE_ID Y EXPEDIENTE_ID, se debe buscar otra verificacion
    IF EXISTS(
        SELECT 1
        FROM "Movimiento"
        WHERE tramite_id = p_tramite_id
        AND expediente_id = p_expediente_id
    ) THEN
        -- Si ya existe, devolver la tupla encontrada
        RETURN QUERY SELECT 
            movimiento_id AS movimientoId, 
            tramite_id AS tramiteId, 
            expediente_id AS expedienteId, 
            usuario_fisico_id AS usuarioFisicoId, 
            usuario_aplicacion_id AS usuarioAplicacionId, 
            area_origen_id AS areaOrigenId, 
            area_destino_id AS areaDestinoId,
            fecha_creacion AS fechaCreacion, 
            observacion_movimiento AS observacionMovimiento, 
            activo AS activo, 
            hash_tabla AS hashTabla;
    ELSE
    -- Si no existe, insertar el nuevo movimiento y devolver la fila insertada
    INSERT INTO "Movimiento" (
        "tramiteId", "expedienteId",  "areaOrigenId", "usuarioFisicoId","usuarioAplicacionId", "areaDestinoId", "observacionMovimiento", "activo","hashTabla"
    ) VALUES (
        p_tramite_id, p_expediente_id, p_area_origen_id , p_usuario_fisico_id, p_usuario_aplicacion_id, p_area_destino_id, p_observacion_movimiento, p_activo, 'HASHDUMP'
    )
    RETURNING "movimientoId", "fechaCreacion" INTO temp_movimientoId, temp_fecha_creacion;

    -- Actualizar fecha ultimo movimiento del expediente
    UPDATE "Expediente"
    SET "fechaUltimoMovimiento" = CURRENT_TIMESTAMP
    WHERE "expedienteId" = p_expediente_id;

    -- Actualizar area actualidad del expediente
    UPDATE "Expediente"
    SET "areaActualidadId" = p_area_destino_id
    WHERE "expedienteId" = p_expediente_id;
    
    -- Actualizar hash de la tabla
    temp_hash_tabla:= "calcularHashExpediente"("p_expediente_id");
    UPDATE "Expediente"
    SET "hashTabla" = "temp_hash_tabla"
    WHERE "expedienteId" = p_expediente_id;

    --Actualizar Hash Movimiento
    temp_hash_tabla:= "calcularHashMovimiento"(temp_movimientoId);
    UPDATE "Movimiento"
    SET "hashTabla" = temp_hash_tabla
    WHERE "movimientoId" = temp_movimientoId;

    -- Devolver la fila completa
    RETURN QUERY SELECT 
        temp_movimientoId AS movimientoId, 
        p_tramite_id AS tramiteId, 
        p_expediente_id AS expedienteId, 
        p_usuario_fisico_id AS usuarioFisicoId, 
        p_usuario_aplicacion_id AS usuarioAplicacionId, 
        p_area_origen_id AS areaOrigenId, 
        p_area_destino_id AS areaDestinoId, 
        temp_fecha_creacion AS fechaCreacion,
        p_observacion_movimiento AS observacionMovimiento, 
        p_activo AS activo, 
        temp_hash_tabla AS hashTabla;
    END IF;
END;
$$;


-- Función obteniendo todos los movimientos por expediente id
CREATE OR REPLACE FUNCTION public."obtenerMovimientosPorExpedienteId"(
    p_expediente_id INT
)
RETURNS TABLE(
    movimiento_id INT,
    tramite_id INT,
    expediente_id INT,
    usuario_fisico_id INT,
    usuario_aplicacion_id INT,
    area_origen_id INT,
    area_destino_id INT,
    fecha_creacion TIMESTAMP,
    observacion_movimiento TEXT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT 
        "movimientoId" AS movimientoId, 
        "tramiteId" AS tramiteId, 
        "expedienteId" AS expedienteId, 
        "usuarioFisicoId" AS usuarioFisicoId, 
        "usuarioAplicacionId" AS usuarioAplicacionId, 
        "areaOrigenId" AS areaOrigenId, 
        "areaDestinoId" AS areaDestinoId, 
        "fechaCreacion" AS fechaCreacion, 
        "observacionMovimiento" AS observacionMovimiento, 
        "Movimiento"."activo" AS activo, 
        "hashTabla" AS hashTabla
    FROM "Movimiento"
    WHERE "expedienteId" = p_expediente_id;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerMovimientos"()
RETURNS TABLE(
    movimiento_id INT,
    tramite_id INT,
    expediente_id INT,
    usuario_fisico_id INT,
    usuario_aplicacion_id INT,
    area_origen_id INT,
    area_destino_id INT,
    fecha_creacion TIMESTAMP,
    observacion_movimiento TEXT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT 
        "movimientoId" AS movimientoId, 
        "tramiteId" AS tramiteId, 
        "expedienteId" AS expedienteId, 
        "usuarioFisicoId" AS usuarioFisicoId, 
        "usuarioAplicacionId" AS usuarioAplicacionId, 
        "areaOrigenId" AS areaOrigenId, 
        "areaDestinoId" AS areaDestinoId, 
        "fechaCreacion" AS fechaCreacion, 
        "observacionMovimiento" AS observacionMovimiento, 
        "Movimiento"."activo" AS activo, 
        "hashTabla" AS hashTabla
    FROM "Movimiento";
END;
$$;