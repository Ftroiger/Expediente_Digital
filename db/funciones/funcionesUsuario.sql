CREATE OR REPLACE FUNCTION public."obtenerUsuarioPorCuil"(
    p_cuil_usuario VARCHAR(100)
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    api_key VARCHAR(100),
    usuario_alta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) AS $$
BEGIN
    -- Realizar consulta y raise exception si no se encuentra el usuario
    RETURN QUERY
    SELECT "usuarioId", "cuilUsuario", "nombreUsuario", "fechaCreacion", "fechaBaja", "areaId", "aplicacionVediId", "apiKey", "usuarioAlta","Usuario"."activo", "hashTabla"
    FROM "Usuario"
    WHERE "cuilUsuario" = p_cuil_usuario;

    -- Si no se encuentra el usuario, devolver un error
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe un usuario con el cuil %', p_cuil_usuario;
    END IF;

    RETURN;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public."obtenerUsuarioPorId"(
    p_usuario_id INT
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    api_key VARCHAR(100),
    usuario_alta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) AS $$
BEGIN
    -- Realizar consulta y raise exception si no se encuentra el usuario
    RETURN QUERY
    SELECT
        "usuarioId" AS usuario_id,
        "cuilUsuario" AS cuil_usuario,
        "nombreUsuario" AS nombre_usuario,
        "fechaCreacion" AS fecha_creacion,
        "fechaBaja" AS fecha_baja,
        "areaId" AS area_id,
        "aplicacionVediId" AS aplicacion_vedi_id,
        "apiKey" AS api_key,
        "usuarioAlta" AS usuario_alta,
        "Usuario"."activo" AS activo,
        "hashTabla" AS hash_tabla
    FROM "Usuario"
    WHERE "usuarioId" = p_usuario_id;

    -- Si no se encuentra el usuario, devolver un error
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe un usuario con el id %', p_usuario_id;
    END IF;
    RETURN;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public."verificarExistenciaUsuarioAplicacion"(
    p_usuario_id INT,
    p_api_key VARCHAR(100)
) RETURNS TABLE (
    existe BOOLEAN -- Detalla el estado del usuario
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar si el usuario existe
    IF NOT EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "usuarioId" = p_usuario_id
    ) THEN
        RAISE EXCEPTION 'No existe un usuario con el usuarioId %', p_usuario_id;
    END IF;

    -- Verificar si el usuario tiene una API Key válida
    IF NOT EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "usuarioId" = p_usuario_id
        AND "apiKey" = p_api_key
    ) THEN
        RAISE EXCEPTION 'La API Key no se encuentra válida';
    END IF;

    -- Verificar si el usuario está asociado a una aplicación
    IF NOT EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "usuarioId" = p_usuario_id
        AND "apiKey" = p_api_key
        AND "aplicacionVediId" IS NOT NULL
    ) THEN
        RAISE EXCEPTION 'El usuario no está asociado a una aplicación';
    END IF;

    -- Si todas las condiciones se cumplen
    RETURN QUERY SELECT TRUE;
END;
$$;

CREATE OR REPLACE FUNCTION public."verificarExistenciaUsuario"(
    p_usuario_id INT
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar si el usuario existe y está activo
    RETURN EXISTS (
        SELECT 1
        FROM "Usuario"
        WHERE "usuarioId" = p_usuario_id
        AND "Usuario"."activo" = TRUE
    );
    RETURN TRUE;
END;
$$;

CREATE OR REPLACE FUNCTION public."verificarExistenciaUsuarioPorCuil"(
    p_usuario_cuil VARCHAR(100)
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar si el usuario existe y está activo
    RETURN EXISTS (
        SELECT 1
        FROM "Usuario"
        WHERE "cuilUsuario" = p_usuario_cuil
        AND "Usuario"."activo" = TRUE
    );
    RETURN TRUE;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerUsuariosPorRol"(
    p_rol_id INT
) RETURNS TABLE (
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    api_key VARCHAR(100),
    usuarioAlta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
BEGIN
    -- Verificar que existe el rol
    IF NOT EXISTS(
        SELECT 1
        FROM "Rol"
        WHERE "rolId" = p_rol_id
    ) THEN
        RAISE EXCEPTION 'No existe un rol con el rolId %', p_rol_id;
    END IF;

    -- Seleccionar los usuarios asociados al rol
    RETURN QUERY
    SELECT
        "Usuario"."usuarioId" AS usuario_id,
        "Usuario"."cuilUsuario" AS cuil_usuario,
        "Usuario"."nombreUsuario" AS nombre_usuario,
        "Usuario"."fechaCreacion" AS fecha_creacion,
        "Usuario"."fechaBaja" AS fecha_baja,
        "Usuario"."areaId" AS area_id,
        "Usuario"."aplicacionVediId" AS aplicacion_vedi_id,
        "Usuario"."apiKey" AS api_key,
        "Usuario"."usuarioAlta" AS usuario_alta,
        "Usuario"."activo" AS activo,
        "Usuario"."hashTabla" AS hash_tabla
    FROM "Usuario"
    JOIN "RolXUsuario" ON "Usuario"."usuarioId" = "RolXUsuario"."usuarioId"
    WHERE "RolXUsuario"."rolId" = p_rol_id;

    -- Si no se encontraron usuarios, lanzar excepción
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existen usuarios con el rolId %', p_rol_id;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerUsuarios"(
    "p_skip" INT,
    "p_limit" INT
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    api_key VARCHAR(100),
    usuario_alta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
BEGIN
    -- Seleccionar los usuarios
    RETURN QUERY
    SELECT
        "usuarioId" AS usuario_id,
        "cuilUsuario" AS cuil_usuario,
        "nombreUsuario" AS nombre_usuario,
        "fechaCreacion" AS fecha_creacion,
        "fechaBaja" AS fecha_baja,
        "areaId" AS area_id,
        "aplicacionVediId" AS aplicacion_vedi_id,
        "apiKey" AS api_key,
        "usuarioAlta" AS usuario_alta,
        "Usuario"."activo" AS activo,
        "hashTabla" AS hash_tabla
    FROM "Usuario"
    ORDER BY "usuarioId" ASC
    OFFSET p_skip
    LIMIT p_limit;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerUsuarioPorAplicacionVediId"(
    p_aplicacion_vedi_id INT
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    api_key VARCHAR(100),
    usuarioAlta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
BEGIN
    -- Seleccionar los usuarios
    RETURN QUERY
    SELECT
        "usuarioId" AS usuario_id,
        "cuilUsuario" AS cuil_usuario,
        "nombreUsuario" AS nombre_usuario,
        "fechaCreacion" AS fecha_creacion,
        "fechaBaja" AS fecha_baja,
        "areaId" AS area_id,
        "aplicacionVediId" AS aplicacion_vedi_id,
        "apiKey" AS api_key,
        "usuarioAlta" AS usuario_alta,
        "Usuario"."activo" AS activo,
        "hashTabla" AS hash_tabla
    FROM "Usuario"
    WHERE "aplicacionVediId" = p_aplicacion_vedi_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe un usuario con la aplicación VEDI ID %', p_aplicacion_vedi_id;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION public."crearUsuarioSuperAdmin"(
    p_cuil_usuario VARCHAR(100),
    p_nombre_usuario VARCHAR(100),
    p_area_id INT,
    p_usuario_alta INT
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    usuario_alta INT,
    aplicacion_vedi_id INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
DECLARE
    temp_usuario_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_rol_x_usuario_id INT;
    temp_fecha_baja TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
    temp_activo BOOLEAN;
    temp_rol_id INT;
    temp_aplicacion_vedi_id INT;        
BEGIN
    -- Verificar si el usuario ya existe
    IF EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "cuilUsuario" = p_cuil_usuario
    ) THEN
        RAISE EXCEPTION 'El usuario ya existe';
    END IF;

    -- Insertar usuario
    INSERT INTO "Usuario"(
        "cuilUsuario",
        "nombreUsuario",
        "areaId",
        "usuarioAlta",
        "activo",
        "hashTabla"
    ) VALUES(
        p_cuil_usuario,
        p_nombre_usuario,
        p_area_id,
        p_usuario_alta,
        TRUE,
        'HASHDUMP'
    ) RETURNING "usuarioId", "fechaCreacion", "fechaBaja", "Usuario"."activo", "aplicacionVediId" 
        INTO 
        temp_usuario_id, temp_fecha_creacion, temp_fecha_baja, temp_activo, temp_aplicacion_vedi_id;

    -- Actualizar el hash de la tabla
    temp_hash_tabla:= "calcularHashUsuario"(temp_usuario_id);
    UPDATE "Usuario"
    SET "hashTabla" = temp_hash_tabla
    WHERE "usuarioId" = temp_usuario_id;

    -- Obtener el rolId del rol 'Super Administrador'
    SELECT "rolId" INTO temp_rol_id FROM "Rol"
    WHERE "nombreRol" = 'Super Admin';

    --verificar que el rol existe
    IF temp_rol_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró el rol Super Admin';
    END IF;

    -- Insertar en la tabla intermedia RolXUsuario
    INSERT INTO "RolXUsuario" ("rolId", "usuarioId", "activo", "hashTabla")
    VALUES (temp_rol_id, temp_usuario_id, TRUE, 'HASHDUMP')
    RETURNING "rolXUsuarioId" INTO temp_rol_x_usuario_id;

    -- Calcular el hash de la tabla
    UPDATE "RolXUsuario"
    SET "hashTabla" = "calcularHashRolXUsuario"(temp_rol_x_usuario_id)
    WHERE "rolXUsuarioId" = temp_rol_x_usuario_id; 

    -- Devolver la fila completa
    RETURN QUERY SELECT 
        temp_usuario_id AS usuario_id, 
        p_cuil_usuario AS cuil_usuario, 
        p_nombre_usuario AS nombre_usuario, 
        temp_fecha_creacion AS fecha_creacion, 
        temp_fecha_baja AS fecha_baja, 
        p_area_id AS area_id, 
        p_usuario_alta AS usuario_alta,
        temp_aplicacion_vedi_id AS aplicacion_vedi_id, 
        temp_activo AS activo,
        temp_hash_tabla AS hash_tabla;
END;
$$;

CREATE OR REPLACE FUNCTION public."crearUsuarioAdministrador"(
    p_cuil_usuario VARCHAR(100),
    p_nombre_usuario VARCHAR(100),
    p_area_id INT,
    p_usuario_alta INT
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    usuario_alta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
DECLARE
    temp_usuario_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_fecha_baja TIMESTAMP;
    temp_rol_x_usuario_id INT;
    temp_hash_tabla VARCHAR(100);
    temp_activo BOOLEAN;
    temp_rol_id INT;
    temp_aplicacion_vedi_id INT;
BEGIN
    -- Verificar si el usuario ya existe
    IF EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "cuilUsuario" = p_cuil_usuario
    ) THEN
        RAISE EXCEPTION 'El usuario ya existe';
    END IF;

    -- Insertar usuario
    INSERT INTO "Usuario"(
        "cuilUsuario",
        "nombreUsuario",
        "areaId",
        "usuarioAlta",
        "activo",
        "hashTabla"
    ) VALUES(
        p_cuil_usuario,
        p_nombre_usuario,
        p_area_id,
        p_usuario_alta,
        TRUE,
        'HASHDUMP'
    ) RETURNING "usuarioId", "fechaCreacion", "fechaBaja", "Usuario"."activo", "aplicacionVediId" 
        INTO 
        temp_usuario_id, temp_fecha_creacion, temp_fecha_baja, temp_activo, temp_aplicacion_vedi_id;

    -- Actualizar el hash de la tabla
    temp_hash_tabla:= "calcularHashUsuario"(temp_usuario_id);
    UPDATE "Usuario"
    SET "hashTabla" = temp_hash_tabla
    WHERE "usuarioId" = temp_usuario_id;

    -- Obtener el rolId del rol 'Administrador'
    SELECT "rolId" INTO temp_rol_id FROM "Rol"
    WHERE "nombreRol" = 'Administrador';

    -- Verificar que el rol existe
    IF temp_rol_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró el rol Administrador';
    END IF;
    
    -- Insertar en la tabla intermedia RolXUsuario
    INSERT INTO "RolXUsuario" ("rolId", "usuarioId", "activo", "hashTabla")
    VALUES (temp_rol_id, temp_usuario_id, TRUE, 'HASHDUMP')
    RETURNING "rolXUsuarioId" INTO temp_rol_x_usuario_id;

    -- Calcular el hash de la tabla
    UPDATE "RolXUsuario"
    SET "hashTabla" = "calcularHashRolXUsuario"(temp_rol_x_usuario_id)
    WHERE "rolXUsuarioId" = temp_rol_x_usuario_id;


    -- Devolver la fila completa
    RETURN QUERY SELECT 
        temp_usuario_id AS usuario_id, 
        p_cuil_usuario AS cuil_usuario, 
        p_nombre_usuario AS nombre_usuario, 
        temp_fecha_creacion AS fecha_creacion, 
        temp_fecha_baja AS fecha_baja, 
        p_area_id AS area_id,
        temp_aplicacion_vedi_id AS aplicacion_vedi_id, 
        p_usuario_alta AS usuario_alta,
        temp_activo AS activo,
        temp_hash_tabla AS hash_tabla;  
END;
$$;



CREATE OR REPLACE FUNCTION public."crearUsuario"(
    p_nombre_usuario VARCHAR(50),
    p_cuil_usuario VARCHAR(100),
    p_area_id INT,
    p_usuario_alta INT,
    p_rol_usuario_id INT
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    usuario_alta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
DECLARE
    temp_usuario_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_fecha_baja TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
    temp_activo BOOLEAN;
    temp_rol_x_usuario_id INT;
    temp_aplicacion_vedi_id INT;
BEGIN
    -- Verificar si el usuario ya existe
    IF EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "cuilUsuario" = p_cuil_usuario
    ) THEN
        RAISE EXCEPTION 'El usuario ya existe';
    END IF;

    -- Insertar usuario
    INSERT INTO "Usuario"(
        "nombreUsuario",
        "cuilUsuario",
        "areaId",
        "usuarioAlta",
        "activo",
        "hashTabla"
    ) VALUES(
        p_nombre_usuario,
        p_cuil_usuario,
        p_area_id,
        p_usuario_alta,
        TRUE,
        'HASHDUMP'
    ) RETURNING "usuarioId", "fechaCreacion", "fechaBaja", "Usuario"."activo", "aplicacionVediId" 
        INTO 
        temp_usuario_id, temp_fecha_creacion, temp_fecha_baja, temp_activo, temp_aplicacion_vedi_id;

    -- Actualizar el hash de la tabla
    temp_hash_tabla:= "calcularHashUsuario"(temp_usuario_id);
    UPDATE "Usuario"
    SET "hashTabla" = temp_hash_tabla
    WHERE "usuarioId" = temp_usuario_id;


    -- Insertar en la tabla intermedia RolXUsuario
    INSERT INTO "RolXUsuario" ("rolId", "usuarioId", "activo", "hashTabla")
    VALUES (p_rol_usuario_id, temp_usuario_id, TRUE, 'HASHDUMP')
    RETURNING "rolXUsuarioId" INTO temp_rol_x_usuario_id;

    -- Calcular el hash de la tabla
    UPDATE "RolXUsuario"
    SET "hashTabla" = "calcularHashRolXUsuario"(temp_rol_x_usuario_id)
    WHERE "rolXUsuarioId" = temp_rol_x_usuario_id;

    -- Devolver la fila completa
    RETURN QUERY SELECT 
        temp_usuario_id AS usuario_id, 
        p_cuil_usuario AS cuil_usuario, 
        p_nombre_usuario AS nombre_usuario, 
        temp_fecha_creacion AS fecha_creacion,
        temp_fecha_baja AS fecha_baja,
        p_area_id AS area_id,
        temp_aplicacion_vedi_id AS aplicacion_vedi_id,
        p_usuario_alta AS usuario_alta,
        temp_activo AS activo,
        temp_hash_tabla AS hash_tabla;
END;
$$;


CREATE OR REPLACE FUNCTION public."crearUsuarioAplicacion"(
    p_usuario_alta_id INT,
    p_nombre_usuario VARCHAR(50),
    p_area_id INT,
    p_aplicacion_vedi_id INT,
    p_api_key VARCHAR(100)
) RETURNS TABLE(
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    api_key VARCHAR(100),
    usuario_alta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
DECLARE
    temp_usuario_id INT;
    temp_activo BOOLEAN;
    temp_fecha_creacion TIMESTAMP;
    temp_fecha_baja TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
    temp_rol_id INT;
    temp_rol_x_usuario_id INT;
BEGIN
    -- Verificar si el usuario aplicacion ya existe
    IF EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "aplicacionVediId" = p_aplicacion_vedi_id
        AND "Usuario"."activo" = TRUE
    ) THEN
        RAISE EXCEPTION 'El sistema vertical ya posee una aplicación asociada';
    END IF;

    -- Si el usuario aplicacion ya existe pero tiene activo en false, se reactiva y se actualiza la fecha de baja
    -- Y se devuelve la tupla
    IF EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "aplicacionVediId" = p_aplicacion_vedi_id
        AND "Usuario"."activo" = FALSE
    ) THEN
        UPDATE "Usuario"
        SET
            "activo" = TRUE,
            "fechaBaja" = NULL
        WHERE
            "aplicacionVediId" = p_aplicacion_vedi_id
        RETURNING
            "usuarioId",
            "fechaCreacion",
            "fechaBaja",
            "Usuario"."activo"
        INTO
            temp_usuario_id,
            temp_fecha_creacion,
            temp_fecha_baja,
            temp_activo;

        -- Actualizar el hash de la tabla
        temp_hash_tabla := "calcularHashUsuario"(temp_usuario_id);
        UPDATE "Usuario"
        SET
            "hashTabla" = temp_hash_tabla
        WHERE
            "usuarioId" = temp_usuario_id;

        -- Obtener los datos del usuario
        RETURN QUERY
        SELECT
            temp_usuario_id,
            "cuilUsuario",
            "nombreUsuario",
            temp_fecha_creacion,
            temp_fecha_baja,
            "areaId",
            "aplicacionVediId",
            "apiKey",
            "usuarioAlta",
            temp_activo,
            temp_hash_tabla
        FROM
            "Usuario"
        WHERE
            "usuarioId" = temp_usuario_id;
        RETURN;
    END IF;


    -- Insertar el usuario
    INSERT INTO "Usuario"(
        "nombreUsuario",
        "areaId",
        "aplicacionVediId",
        "apiKey",
        "usuarioAlta",
        "activo",
        "hashTabla"
    ) VALUES(
        p_nombre_usuario,
        p_area_id,
        p_aplicacion_vedi_id,
        p_api_key,
        p_usuario_alta_id,
        TRUE,
        'HASHDUMP'
    )
    RETURNING
        "usuarioId",
        "Usuario"."activo",
        "fechaCreacion",
        "fechaBaja"
    INTO
        temp_usuario_id,
        temp_activo,
        temp_fecha_creacion,
        temp_fecha_baja;

    -- Actualizar el hash de la tabla
    temp_hash_tabla :="calcularHashUsuario"(temp_usuario_id);
    UPDATE "Usuario"
    SET
        "hashTabla" = temp_hash_tabla
    WHERE
        "usuarioId" = temp_usuario_id;

    
    -- Llamar rol de Usuario Aplicacion

    -- Obtener el rolId del rol 'Usuario Aplicacion'
    SELECT "rol_id" INTO temp_rol_id FROM public."obtenerRolPorNombre"('Usuario Aplicacion');

    -- Verificar que el rol existe
    IF temp_rol_id IS NULL THEN
        RAISE EXCEPTION 'No se encontró el rol Usuario Aplicacion';
    END IF;

    -- Insertar en la tabla intermedia RolXUsuario
    INSERT INTO "RolXUsuario" ("rolId", "usuarioId", "activo", "hashTabla")
    VALUES (temp_rol_id, temp_usuario_id, TRUE, 'HASHDUMP')
    RETURNING "rolXUsuarioId" INTO temp_rol_x_usuario_id;

    -- Calcular el hash de la tabla
    UPDATE "RolXUsuario"
    SET
        "hashTabla" = "calcularHashRolXUsuario"(temp_rol_x_usuario_id)
    WHERE
        "rolXUsuarioId" = temp_rol_x_usuario_id;

    
    -- Obtener los datos del usuario
    RETURN QUERY
    SELECT
        temp_usuario_id,
        "cuilUsuario",
        "nombreUsuario",
        temp_fecha_creacion,
        temp_fecha_baja,
        "areaId",
        "aplicacionVediId",
        "apiKey",
        "usuarioAlta",
        temp_activo,
        temp_hash_tabla
    FROM
        "Usuario"
    WHERE
        "usuarioId" = temp_usuario_id;

END;
$$;


CREATE OR REPLACE FUNCTION public."darBajaUsuarioAplicacion"(
    p_usuario_aplicacion_id INT
) RETURNS TABLE (
    usuario_id INT,
    cuil_usuario VARCHAR(100),
    nombre_usuario VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_baja TIMESTAMP,
    area_id INT,
    aplicacion_vedi_id INT,
    api_key VARCHAR(100),
    usuario_alta INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql AS $$
DECLARE
    --temp_usuario_id INT;
    temp_activo BOOLEAN;
    temp_fecha_creacion TIMESTAMP;
    temp_fecha_baja TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
    temp_rol_x_usuario_id INT;
BEGIN
    -- Verificar si el usuario aplicacion ya existe y se encuentra activo
    IF NOT EXISTS(
        SELECT 1
        FROM "Usuario"
        WHERE "aplicacionVediId" IS NOT NULL AND
        "Usuario"."activo" = TRUE
    ) THEN
        RAISE EXCEPTION 'El usuario aplicacion no existe';
    END IF;

    -- Dar de baja al usuario
    UPDATE "Usuario"
    SET
        "activo" = FALSE,
        "fechaBaja" = NOW()
    WHERE
        "usuarioId" = p_usuario_aplicacion_id;

    -- Actualizar el hash de la tabla
    temp_hash_tabla := "calcularHashUsuario"(p_usuario_aplicacion_id);
    UPDATE "Usuario"
    SET
        "hashTabla" = temp_hash_tabla
    WHERE
        "usuarioId" = p_usuario_aplicacion_id;
    
    -- actualizar estado de la tabla RolXUsuario
    UPDATE "RolXUsuario"
    SET
        "activo" = FALSE
    WHERE
        "usuarioId" = p_usuario_aplicacion_id;
    
    -- Obtener Id RolXUsuario
    SELECT "rolXUsuarioId" INTO temp_rol_x_usuario_id 
    FROM "RolXUsuario" 
    WHERE "usuarioId" = p_usuario_aplicacion_id;

    -- Actualizar el hash de la tabla RolXUsuario
    temp_hash_tabla := "calcularHashRolXUsuario"(temp_rol_x_usuario_id);
    UPDATE "RolXUsuario"
    SET
        "hashTabla" = temp_hash_tabla
    WHERE
        "rolXUsuarioId" = temp_rol_x_usuario_id;

    -- Borrar la notificación correspondiente a este pedido de baja
    DELETE FROM "Notificacion" n
    USING "TipoNotificacion" tn
    WHERE n."tipoNotificacionId" = tn."tipoNotificacionId"
    AND tn."nombreTipoNotificacion" = 'Baja'
    AND n."usuarioAfectadoId" = p_usuario_aplicacion_id;


    -- Retornar objeto completo usuario que se dio de baja
    RETURN QUERY
    SELECT
        "usuarioId",
        "cuilUsuario",
        "nombreUsuario",
        "fechaCreacion",
        "fechaBaja",
        "areaId",
        "aplicacionVediId",
        "apiKey",
        "usuarioAlta",
        "Usuario"."activo",
        "hashTabla"
    FROM
        "Usuario"
    WHERE
        "usuarioId" = p_usuario_aplicacion_id;

END;
$$;