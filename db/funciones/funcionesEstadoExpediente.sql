/* FUNCIONES ALMACENADAS PARA EL TIPO DE EXPEDIENTE */

CREATE OR REPLACE FUNCTION public."obtenerEstadoExpedientePorNombre"(
    p_nombre_estado_expediente VARCHAR(50)
) RETURNS TABLE(
    estado_expediente_id INT,
    nombre_estado_expediente VARCHAR(50),
    descripcion_estado_expediente VARCHAR(100),
    activo BOOLEAN
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- Variables para guardar el query
    v_estado_expediente_id INT;
    v_nombre_estado_expediente VARCHAR(50);
    v_descripcion_estado_expediente VARCHAR(100);
    v_activo BOOLEAN;
BEGIN
    SELECT "estadoExpedienteId", "nombreEstadoExpediente", "descripcionEstadoExpediente", "EstadoExpediente".activo
    INTO v_estado_expediente_id, v_nombre_estado_expediente, v_descripcion_estado_expediente, v_activo
    FROM "EstadoExpediente"
    WHERE "nombreEstadoExpediente" = p_nombre_estado_expediente;

    -- Si no se encuentra el estado de expediente
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe ese estado de expediente';
    END IF;

    -- Si se encuentra pero no está activo
    IF NOT v_activo THEN
        RAISE EXCEPTION 'El estado de expediente se encuentra inactivo';
    END IF;

    RETURN QUERY SELECT v_estado_expediente_id, v_nombre_estado_expediente, v_descripcion_estado_expediente, v_activo;
END;
$$;
