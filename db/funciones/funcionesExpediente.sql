/* PROCEDIMIENTOS ALMACENADOS PARA AUTOMATIZAR CARGAR LOS DATOS EN LA TABLA EXPEDIENTE */

CREATE OR REPLACE FUNCTION public."crearExpediente"(
    p_tipo_expediente_id INT,
    p_expediente_padre_id INT,
    p_numero_expediente VARCHAR(100),
    p_area_iniciadora_id INT,
    p_usuario_creador_fisico_id INT,
    p_usuario_creador_aplicacion_id INT,
    p_asunto_expediente VARCHAR(100),
    p_visibilidad_expediente VARCHAR(100),
    p_activo BOOLEAN,
    p_tema_nombre VARCHAR(100),
    p_folios_apertura INT,
    p_folios_actuales INT,
    p_documento_sirad_id INT
)RETURNS TABLE(
    expediente_id INT,
    tipo_expediente_id INT,
    expediente_padre_id INT,
    numero_expediente VARCHAR(100),
    area_iniciadora_id INT,
    usuario_creador_fisico_id INT,
    usuario_creador_aplicacion_id INT,
    asunto_expediente VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_ultimo_movimiento TIMESTAMP,
    visibilidad_expediente VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100),
    tema_nombre VARCHAR(100),
    area_actualidad_id INT,
    folios_apertura INT,
    folios_actuales INT,
    documento_sirad_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    temp_expediente_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_fecha_ultimo_movimiento TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
    temp_estado_id INT;
    temp_historial_id INT;
    temp_fecha_desde TIMESTAMP;
    temp_activo_historial BOOLEAN;
BEGIN
    --Verificar si ya existe un expediente con el mismo numeroExpediente
    IF EXISTS(
        SELECT 1
        FROM "Expediente"
        WHERE numero_expediente = p_numero_expediente
    )THEN
        -- Si ya existe, devuelve una excepcion con el numero de exediente
        RAISE EXCEPTION 'Ya existe expediente con este numero de expediente %', p_numero_expediente;
    ELSE
        -- Si no existe, insertar el nuevo expediente y devolver la fila insertada
        INSERT INTO "Expediente"(
            "tipoExpedienteId", "expedientePadreId", "numeroExpediente", "areaIniciadoraId","usuarioCreadorFisicoId" ,"usuarioCreadorAplicacionId", "asuntoExpediente", "visibilidadExpediente", "activo", "foliosApertura", "documentoSiradId", "foliosActuales", "areaActualidadId","temaNombre","hashTabla"
        ) VALUES(
            p_tipo_expediente_id, p_expediente_padre_id, p_numero_expediente, p_area_iniciadora_id,p_usuario_creador_fisico_id ,p_usuario_creador_aplicacion_id, p_asunto_expediente, p_visibilidad_expediente, p_activo, p_folios_apertura, p_documento_sirad_id, p_folios_apertura, p_area_iniciadora_id,p_tema_nombre,'HASHDUMP'
        )
        RETURNING "expedienteId", "fechaCreacion", "fechaUltimoMovimiento" INTO temp_expediente_id, temp_fecha_creacion, temp_fecha_ultimo_movimiento;
        
        --Agregar Hash
        temp_hash_tabla:="calcularHashExpediente"("temp_expediente_id");
        UPDATE "Expediente"
        SET "hashTabla" = temp_hash_tabla
        WHERE "expedienteId" = temp_expediente_id;
        -- Obtener el id de estado para un estado 'creado'
        SELECT "estadoExpedienteId"
        INTO temp_estado_id
        FROM "EstadoExpediente"
        WHERE "nombreEstadoExpediente" = 'Creado';
        -- Error si no se encuentra el estado
        IF NOT FOUND THEN
            RAISE EXCEPTION 'No se encontro el estado con el nombre de estado Creado';
        END IF;

        -- Insertar el nuevo estado del expediente en la tabla HistorialEstadoExpediente
        INSERT INTO "HistorialEstadoExpediente"(
            "estadoExpedienteId", "expedienteId", "fechaHasta", "activo","hashTabla"
        ) VALUES(
            temp_estado_id, temp_expediente_id, temp_fecha_ultimo_movimiento, TRUE,'HASHDUMP'
        )
        RETURNING "historialEstadoExpedienteId", "fechaDesde","HistorialEstadoExpediente"."activo" into temp_historial_id , temp_fecha_desde, temp_activo_historial;

        --Agregar Hash
        temp_hash_tabla:= "calcularHashHistorialEstadoExpediente"(temp_historial_id);
        UPDATE "HistorialEstadoExpediente"
        SET "hashTabla" = temp_hash_tabla
        WHERE "expedienteId" = temp_historial_id;
        
        --Devolver la fila Completa
        RETURN QUERY SELECT
            temp_expediente_id AS expediente_id,
            p_tipo_expediente_id AS tipo_expediente_id,
            p_expediente_padre_id AS expediente_padre_id,
            p_numero_expediente AS numero_expediente,
            p_area_iniciadora_id AS area_iniciadora_id,
            p_usuario_creador_fisico_id AS usuario_creador_fisico_id,
            p_usuario_creador_aplicacion_id AS usuario_creador_aplicacion_id,
            p_asunto_expediente AS asunto_expediente,
            temp_fecha_creacion AS fecha_creacion,
            temp_fecha_ultimo_movimiento AS fecha_ultimo_movimiento,
            p_visibilidad_expediente AS visibilidad_expediente,
            p_activo AS activo,
            temp_hash_tabla AS hash_tabla,
            p_tema_nombre AS tema_nombre,
            p_area_iniciadora_id AS area_actualidad_id,
            p_folios_apertura AS folios_apertura,
            p_folios_actuales AS folios_actuales,
            p_documento_sirad_id AS documento_sirad_id;
    END IF;
END;
$$;

-- Función para buscar todos los expedientes 
CREATE OR REPLACE FUNCTION public."obtenerExpedientes"(
    p_skip INT,
    p_limit INT
) RETURNS TABLE(
    expediente_id INT,
    tipo_expediente_id INT,
    expediente_padre_id INT,
    numero_expediente VARCHAR(100),
    area_iniciadora_id INT,
    usuario_creador_fisico_id INT,
    usuario_creador_aplicacion_id INT,
    asunto_expediente VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_ultimo_movimiento TIMESTAMP,
    visibilidad_expediente VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100),
    tema_nombre VARCHAR(100),
    area_actualidad_id INT,
    folios_apertura INT,
    folios_actuales INT,
    documento_sirad_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        "expedienteId",
        "tipoExpedienteId",
        "expedientePadreId",
        "numeroExpediente",
        "areaIniciadoraId",
        "usuarioCreadorFisicoId",
        "usuarioCreadorAplicacionId",
        "asuntoExpediente",
        "fechaCreacion",
        "fechaUltimoMovimiento",
        "visibilidadExpediente",
        "Expediente"."activo",
        "hashTabla",
        "temaNombre",
        "areaActualidadId",
        "foliosApertura",
        "foliosActuales",
        "documentoSiradId"
    FROM "Expediente"
    ORDER BY "fechaCreacion" DESC
    OFFSET p_skip
    LIMIT p_limit;
END;
$$;

CREATE OR REPLACE FUNCTION public."actualizarFoliosExpediente"(
    p_expediente_id INT,
    p_folios_actuales INT
) RETURNS TABLE(
    expediente_id INT,
    numero_expediente VARCHAR(100),
    folios_actuales INT
)
LANGUAGE plpgsql
AS $$ 
DECLARE
    v_numero_expediente VARCHAR(100);
    v_activo BOOLEAN;
    v_hash_tabla VARCHAR(100);
BEGIN
    -- Buscar el expediente
    SELECT "numeroExpediente", activo
    INTO v_numero_expediente, v_activo
    FROM "Expediente"
    WHERE "expedienteId" = p_expediente_id;

    -- Sino se encuentra el estado de expediente
    IF NOT FOUND THEN 
        RAISE EXCEPTION 'No existe expediente con el id de expediente %', p_expediente_id;
    END IF;

    -- Si se enceuntra pero no está activo
    IF NOT v_activo THEN
        RAISE EXCEPTION 'El expediente se encuentra inactivo';
    END IF;

    UPDATE "Expediente" SET "foliosActuales" = p_folios_actuales
    WHERE "expedienteId" = p_expediente_id;

    --Actualizar hash Tabla
    v_hash_tabla:="calcularHashExpediente"(p_expediente_id);
    UPDATE "Expediente"
    SET "hashTabla" = v_hash_tabla
    WHERE "expedienteId" = p_expediente_id;

    RETURN QUERY SELECT
        p_expediente_id AS expedienteId,
        v_numero_expediente AS numeroExpediente,
        p_folios_actuales AS foliosActuales;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerFoliosActuales"(
    p_expediente_id INT
)
RETURNS TABLE(
    expediente_id INT,
    numero_expediente VARCHAR(100),
    folios_actuales INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS(
        SELECT 1
        FROM "Expediente"
        WHERE "expedienteId" = p_expediente_id
    )THEN
        RAISE EXCEPTION 'No existe expediente con el id de expediente %', p_expediente_id;
    END IF;

    RETURN QUERY SELECT 
        p_expediente_id AS expedienteId,
        "numeroExpediente",
        "foliosActuales"
    FROM "Expediente"
    WHERE "expedienteId" = p_expediente_id;

END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerExpedientePorNumeroExpediente"(
    p_numero_expediente VARCHAR(100)
) 
RETURNS TABLE(
     expediente_id INT,
    tipo_expediente_id INT,
    expediente_padre_id INT,
    numero_expediente VARCHAR(100),
    area_iniciadora_id INT,
    usuario_creador_fisico_id INT,
    usuario_creador_aplicacion_id INT,
    asunto_expediente VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_ultimo_movimiento TIMESTAMP,
    visibilidad_expediente VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100),
    tema_nombre VARCHAR(100),
    area_actualidad_id INT,
    folios_apertura INT,
    folios_actuales INT,
    documento_sirad_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE 
    v_activo BOOLEAN;
BEGIN
    -- Realizar la consulta y retornar el expediente si existe y está activo
    RETURN QUERY
    SELECT 
        e."expedienteId",
        e."tipoExpedienteId",
        e."expedientePadreId",
        e."numeroExpediente",
        e."areaIniciadoraId",
        e."usuarioCreadorFisicoId",
        e."usuarioCreadorAplicacionId",
        e."asuntoExpediente",
        e."fechaCreacion",
        e."fechaUltimoMovimiento",
        e."visibilidadExpediente",
        e."activo",
        e."hashTabla",
        e."temaNombre",
        e."areaActualidadId",
        e."foliosApertura",
        e."foliosActuales",
        e."documentoSiradId"
    FROM "Expediente" e
    WHERE e."numeroExpediente" = p_numero_expediente;

    -- Si no se encontró un expediente activo, verificar si existe uno inactivo
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe el expediente con el numero de expediente %', p_numero_expediente;
    END IF;
END;
$$;

-- Función almacenada para actualizar la area actual del expediente
CREATE OR REPLACE FUNCTION public."actualizarAreaActualidadExpediente"(
    p_expediente_id INT,
    p_area_actualidad_id INT
)
RETURNS TABLE(
    expediente_id INT,
    numero_expediente VARCHAR(100),
    area_actualidad_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_numero_expediente VARCHAR(100);
BEGIN
    SELECT "numeroExpediente"
    INTO v_numero_expediente
    FROM "Expediente"
    WHERE "expedienteId" = p_expediente_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe expediente con el id de expediente %', p_expediente_id;
    END IF;

    UPDATE "Expediente" SET "areaActualidadId" = p_area_actualidad_id
    WHERE "expedienteId" = p_expediente_id;

    RETURN QUERY SELECT
        p_expediente_id AS expedienteId,
        v_numero_expediente AS numeroExpediente,
        p_area_actualidad_id AS areaActualidadId;
END;
$$;

-- Función almacenada para obtener el expediente con id
CREATE OR REPLACE FUNCTION public."obtenerExpedientePorId"(
    p_expediente_id INT
)
RETURNS TABLE(
    expediente_id INT,
    tipo_expediente_id INT,
    expediente_padre_id INT,
    numero_expediente VARCHAR(100),
    area_iniciadora_id INT,
    usuario_creador_fisico_id INT,
    usuario_creador_aplicacion_id INT,
    asunto_expediente VARCHAR(255),
    fecha_creacion TIMESTAMP,
    fecha_ultimo_movimiento TIMESTAMP,
    visibilidad_expediente VARCHAR(50),
    activo BOOLEAN,
    hash_tabla VARCHAR(100),
    area_actualidad_id INT,
    folios_apertura INT,
    folios_actuales INT,
    documento_sirad_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE 
    v_activo BOOLEAN;
BEGIN
    RETURN QUERY
    SELECT 
        "expedienteId",
        "tipoExpedienteId",
        "expedientePadreId",
        "numeroExpediente",
        "areaIniciadoraId",
        "usuarioCreadorFisicoId",
        "usuarioCreadorAplicacionId",
        "asuntoExpediente",
        "fechaCreacion",
        "fechaUltimoMovimiento",
        "visibilidadExpediente",
        "Expediente".activo,
        "hashTabla",
        "areaActualidadId",
        "foliosApertura",
        "foliosActuales",
        "documentoSiradId"
    FROM "Expediente"
    WHERE "expedienteId" = p_expediente_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe expediente con el id de expediente %', p_expediente_id;
    END IF;
END;
$$; 

CREATE OR REPLACE FUNCTION public."verificarExistenciaNumeroExpediente"(
    p_numero_expediente VARCHAR(100)
)
RETURNS TABLE(
    existe BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT EXISTS (
        SELECT 1
        FROM "Expediente"
        WHERE "numeroExpediente" = p_numero_expediente
    ) AS existe;
END;
$$;
