CREATE OR REPLACE FUNCTION public."crearRelacionRolPermiso"(
    p_rol_id INT,
    p_permiso_id INT
)
RETURNS TABLE(
    rol_x_permiso_id INT,
    rol_id INT,
    permiso_id INT,
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
DECLARE 
    temp_rol_x_permiso_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
BEGIN
    -- Verificar si el rol existe
    IF NOT EXISTS(
        SELECT 1
        FROM "Rol"
        WHERE "rolId" = p_rol_id
    ) THEN
        RAISE EXCEPTION 'El rol no existe ID: %', p_rol_id;
    END IF;

    -- Verificar si el permiso existe
    IF NOT EXISTS(
        SELECT 1
        FROM "Permiso"
        WHERE "permisoId" = p_permiso_id
    ) THEN
        RAISE EXCEPTION 'El permiso no existe ID: %', p_permiso_id;
    END IF;

    -- verificar si existe la relacion
    IF EXISTS(
        SELECT 1
        FROM "RolXPermiso"
        WHERE "rolId" = p_rol_id
        AND "permisoId" = p_permiso_id
    ) THEN
        RAISE EXCEPTION 'La relación entre el rol y el permiso ya existe';
    ELSE
        -- crear la relacion
        INSERT INTO "RolXPermiso"(
            "rolId",
            "permisoId",
            "activo",
            "hashTabla"
        ) VALUES(
            p_rol_id,
            p_permiso_id,
            TRUE,
            'HASHDUMP'
        ) RETURNING "rolXPermisoId", "fechaCreacion", "hashTabla" INTO temp_rol_x_permiso_id, temp_fecha_creacion, temp_hash_tabla;

    -- agregar Hash
    temp_hash_tabla := "calcularHashRolXPermiso"(temp_rol_x_permiso_id);
    UPDATE "RolXPermiso"
    SET "hashTabla" = temp_hash_tabla
    WHERE "rolXPermisoId" = temp_rol_x_permiso_id;

    RETURN QUERY SELECT 
        temp_rol_x_permiso_id AS rol_x_permiso_id,
        p_rol_id AS rol_id,
        p_permiso_id AS permiso_id,
        temp_fecha_creacion AS fecha_creacion,
        TRUE AS activo,
        temp_hash_tabla AS hash_tabla;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerRolXPermiso"(
    p_skip INT,
    p_limit INT
)
RETURNS TABLE(
    rol_x_permiso_id INT,
    permiso_id INT,
    rol_id INT,
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT 
        "rolXPermisoId" AS rol_x_permiso_id,
        "permisoId" AS permiso_id,
        "rolId" AS rol_id,
        "fechaCreacion" AS fecha_creacion,
        "RolXPermiso"."activo" AS activo,
        "hashTabla" AS hash_tabla
    FROM "RolXPermiso"
    ORDER BY "fechaCreacion" DESC
    LIMIT p_limit
    OFFSET p_skip;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerPermisosPorNombreRol"(
    p_nombre_rol VARCHAR(50)
)
RETURNS TABLE(
    permiso_id INT,
    nombre_permiso VARCHAR(50),
    descripcion_permiso VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN
) LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar si el rol existe
    IF NOT EXISTS(
        SELECT 1
        FROM "Rol"
        WHERE "nombreRol" = p_nombre_rol
    ) THEN
        RAISE EXCEPTION 'El rol no existe';
    END IF;

    RETURN QUERY SELECT 
        "Permiso"."permisoId" AS permiso_id,
        "Permiso"."nombrePermiso" AS nombre_permiso,
        "Permiso"."descripcionPermiso" AS descripcion_permiso,
        "Permiso"."fechaCreacion" AS fecha_creacion,
        "Permiso"."activo" AS activo
    FROM "RolXPermiso"
    JOIN "Permiso" ON "RolXPermiso"."permisoId" = "Permiso"."permisoId"
    JOIN "Rol" ON "RolXPermiso"."rolId" = "Rol"."rolId"
    WHERE "Rol"."nombreRol" = p_nombre_rol
    ORDER BY "Permiso"."fechaCreacion" DESC;
END;
$$;

CREATE OR REPLACE FUNCTION public."eliminarRolXPermisoPorPermisoId"(
    p_permiso_id INT
)
RETURNS TABLE(
    rolXPermisoId INT,
    rolId INT,
    permisoId INT,
    fechaCreacion TIMESTAMP,
    activo BOOLEAN,
    hashTabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
DECLARE
    temp_rol_x_permiso RECORD;
    updated_rows RECORD;
BEGIN
    -- Verificar si existe la relación
    IF NOT EXISTS(
        SELECT 1
        FROM "RolXPermiso"
        WHERE "permisoId" = p_permiso_id
    ) THEN
        RAISE EXCEPTION 'La relación entre el rol y el permiso no existe';
    END IF;

    -- Actualizar estado a inactivo en la tabla RolXPermiso para las relaciones con el permiso
    FOR temp_rol_x_permiso IN
        UPDATE "RolXPermiso"
        SET "activo" = FALSE
        WHERE "permisoId" = p_permiso_id
        RETURNING "rolXPermisoId", "rolId", "permisoId", "fechaCreacion", "RolXPermiso"."activo"
    LOOP
        -- Actualizar el hash para cada tupla modificada
        UPDATE "RolXPermiso"
        SET "hashTabla" = "calcularHashRolXPermiso"(temp_rol_x_permiso."rolXPermisoId")
        WHERE "rolXPermisoId" = temp_rol_x_permiso."rolXPermisoId";

        -- Devolver las filas modificadas, guardando los resultados
        RETURN QUERY 
        SELECT temp_rol_x_permiso."rolXPermisoId", 
               temp_rol_x_permiso."rolId", 
               temp_rol_x_permiso."permisoId", 
               temp_rol_x_permiso."fechaCreacion", 
               temp_rol_x_permiso."activo", 
               "calcularHashRolXPermiso"(temp_rol_x_permiso."rolXPermisoId") AS "hashTabla";
    END LOOP;

END;
$$;

CREATE OR REPLACE FUNCTION public."eliminarRolXPermisoPorRolId"(
    p_rol_id INT
)
RETURNS TABLE(
    rol_x_permiso_id INT,
    rol_id INT,
    permiso_id INT,
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
DECLARE
    temp_rol_x_permiso RECORD;
    updated_rows RECORD;
BEGIN
    -- Verificar si existe la relación
    IF NOT EXISTS(
        SELECT 1
        FROM "RolXPermiso"
        WHERE "rolId" = p_rol_id
    ) THEN
        RAISE EXCEPTION 'La relación entre el rol y el permiso no existe';
    END IF;

    -- Actualizar estado a inactivo en la tabla RolXPermiso para las relaciones con el rol
    FOR temp_rol_x_permiso IN
        UPDATE "RolXPermiso"
        SET "activo" = FALSE
        WHERE "rolId" = p_rol_id
        RETURNING "rolXPermisoId", "rolId", "permisoId", "fechaCreacion", "RolXPermiso"."activo"
    LOOP
        -- Actualizar el hash para cada tupla modificada
        UPDATE "RolXPermiso"
        SET "hashTabla" = "calcularHashRolXPermiso"(temp_rol_x_permiso."rolXPermisoId")
        WHERE "rolXPermisoId" = temp_rol_x_permiso."rolXPermisoId";

        -- Devolver las filas modificadas, guardando los resultados
        RETURN QUERY 
        SELECT temp_rol_x_permiso."rolXPermisoId" AS rol_x_permiso_id, 
               temp_rol_x_permiso."rolId" AS rol_id, 
               temp_rol_x_permiso."permisoId" AS permiso_id, 
               temp_rol_x_permiso."fechaCreacion" AS fecha_creacion, 
               temp_rol_x_permiso."activo" as activo, 
               "calcularHashRolXPermiso"(temp_rol_x_permiso."rolXPermisoId") AS hash_tabla;
    END LOOP;

END;
$$;