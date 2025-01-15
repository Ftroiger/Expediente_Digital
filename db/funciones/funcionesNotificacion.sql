/*
Función almacenada para crear una notificación tipo 'Baja'.

Parámetros de entrada:
    - usuarioId: Identificador del usuario que realiza la acción.
    - descripcionNotificacion: Descripción de la notificación.

Parámetros de salida:
    - notificacionId: Identificador de la notificación creada.
    - usuarioNotificadoId: Identificador del usuario que recibe la notificación.
    - tipoNotificacionId: Tipo de notificación creada.
    - descripcionNotificacion: Descripción de la notificación creada.
    - usuarioAfectadoId: Identificador del usuario afectado por la notificación.
    - leido: Estado de lectura de la notificación.
    - fechaCreacion: Fecha de creación de la notificación.
    - activo: Estado de activación de la notificación.
    - hashTabla: Hash de la tabla de la notificación.

*/
CREATE OR REPLACE FUNCTION public."crearNotificacionBaja"(
    p_usuario_notificador_id INT,
    p_usuario_afectado_id INT, 
    p_descripcion_notificacion VARCHAR(255))
RETURNS TABLE(
    notificacion_id INT,
    usuario_notificado_id INT,
    tipo_notificacion_id INT,
    descripcion_notificacion VARCHAR(255),
    usuario_afectado_id INT,
    leido BOOLEAN,  
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
DECLARE
    temp_notificacion_tipo_id INT;
    temp_notificacion_id INT;
    temp_hash_tabla VARCHAR(100);
    temp_usuario_notificado_id INT;
BEGIN
    -- Buscar el identificador del tipo de notificación 'Baja'.
    SELECT "tipoNotificacionId" INTO temp_notificacion_tipo_id
    FROM "TipoNotificacion"
    WHERE "nombreTipoNotificacion" = 'Baja';

    -- Agarrar el usuario notificado
    SELECT "usuarioAlta" INTO temp_usuario_notificado_id
    FROM "Usuario"
    WHERE "usuarioId" = p_usuario_notificador_id;

    -- Crear la notificación.
    INSERT INTO "Notificacion"(
        "usuarioNotificadoId",
        "tipoNotificacionId",
        "descripcionNotificacion",
        "usuarioAfectadoId",
        "leido",
        "fechaCreacion",
        "activo",
        "hashTabla"
    )
    VALUES(
        temp_usuario_notificado_id,
        temp_notificacion_tipo_id,
        p_descripcion_notificacion,
        p_usuario_afectado_id,
        FALSE,
        CURRENT_TIMESTAMP,
        TRUE,
        'HASHDUMP'
    )
    RETURNING "notificacionId" INTO temp_notificacion_id;

    -- Actualizar el hash de la tabla
    temp_hash_tabla:= "calcularHashNotificacion"(temp_notificacion_id);
    UPDATE "Notificacion"
    SET "hashTabla" = temp_hash_tabla
    WHERE "notificacionId" = temp_notificacion_id;


    RETURN QUERY SELECT 
        "notificacionId" AS notificacion_id,
        "usuarioNotificadoId" AS usuario_notificado_id,
        "tipoNotificacionId" AS tipo_notificacion_id,
        "descripcionNotificacion" AS descripcion_notificacion,
        "usuarioAfectadoId" AS usuario_afectado_id,
        "Notificacion"."leido" AS leido,
        "fechaCreacion" AS fecha_creacion,
        "Notificacion"."activo" AS activo,
        "hashTabla" AS hash_tabla   
    FROM "Notificacion"
    WHERE "usuarioNotificadoId" = temp_usuario_notificado_id
    ORDER BY "fechaCreacion" DESC
    LIMIT 1;
END;
$$;

/*
    Funcion que verifica si el usuario ya realizo una solicitud de baja
*/
CREATE OR REPLACE FUNCTION public."verificarSolicitudBaja"(
    p_usuario_afectado_id INT
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Verificar si existe una notificación de baja activa al usuario afectado.
    RETURN EXISTS (
        SELECT 1 
        FROM "Notificacion" n 
        join "TipoNotificacion" tn on n."tipoNotificacionId" = tn."tipoNotificacionId" 
        WHERE tn."nombreTipoNotificacion" = 'Baja'
            AND n."usuarioAfectadoId" = p_usuario_afectado_id
            AND n."activo" = TRUE
    );
END;
$$ LANGUAGE plpgsql;
