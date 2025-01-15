/* FUNCIONES ALMACENADAS PARA EL TIPO DE EXPEDIENTE */

CREATE OR REPLACE FUNCTION public."obtenerTipoExpedientePorNombre"(
    p_nombre_tipo_expediente VARCHAR(50)
) RETURNS TABLE(
    tipo_expediente_id INT,
    nombre_tipo_expediente VARCHAR(50),
    descripcion_tipo_expediente VARCHAR(100),
    activo BOOLEAN
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- Variables para guardar el query
    v_tipo_expediente_id INT;
    v_nombre_tipo_expediente VARCHAR(50);
    v_descripcion_tipo_expediente VARCHAR(100);
    v_activo BOOLEAN;
BEGIN
    SELECT "tipoExpedienteId", "nombreTipoExpediente", "descripcionTipoExpediente", "TipoExpediente".activo
    INTO v_tipo_expediente_id, v_nombre_tipo_expediente, v_descripcion_tipo_expediente, v_activo
    FROM "TipoExpediente"
    WHERE "nombreTipoExpediente" = p_nombre_tipo_expediente;

    -- Si no se encuentra el tipo de expediente
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe ese tipo de expediente';
    END IF;

    RETURN QUERY SELECT v_tipo_expediente_id, v_nombre_tipo_expediente, v_descripcion_tipo_expediente, v_activo;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerTipoExpedientes"()
RETURNS TABLE(
    tipo_expediente_id INT,
    nombre_tipo_expediente VARCHAR(50),
    descripcion_tipo_expediente VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- Variables para guardar el query
    v_tipo_expediente_id INT;
    v_nombre_tipo_expediente VARCHAR(50);
    v_descripcion_tipo_expediente VARCHAR(100);
    v_activo BOOLEAN;
    v_hash_tabla VARCHAR(100);
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "TipoExpediente") 
    THEN
        RAISE EXCEPTION 'No hay tipos de expediente en la base de datos';
        RETURN;
    END IF;
    SELECT "tipoExpedienteId", "nombreTipoExpediente", "descripcionTipoExpediente", "TipoExpediente".activo, "hashTabla"
    INTO v_tipo_expediente_id, v_nombre_tipo_expediente, v_descripcion_tipo_expediente, v_activo, v_hash_tabla
    FROM "TipoExpediente";

    RETURN QUERY SELECT v_tipo_expediente_id, v_nombre_tipo_expediente, v_descripcion_tipo_expediente, v_activo, v_hash_tabla;
END;
$$;


