CREATE OR REPLACE FUNCTION public."obtenerPermisoPorId"(
    p_permiso_id INT
)
RETURNS TABLE(
    permiso_id INT,
    nombre_permiso VARCHAR(50),
    descripcion_permiso VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT 
        "permisoId" AS permisoId, 
        "nombrePermiso" AS nombrePermiso, 
        "descripcionPermiso" AS descripcionPermiso, 
        "fechaCreacion" AS fechaCreacion, 
        "Permiso"."activo" AS activo, 
        "hashTabla" AS hashTabla
    FROM "Permiso"
    WHERE "permisoId" = p_permiso_id;
END;
$$;


CREATE OR REPLACE FUNCTION public."obtenerPermisos"(
    p_skip INT,
    p_limit INT
)
RETURNS TABLE(
    permiso_id INT,
    nombre_permiso VARCHAR(50),
    descripcion_permiso VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        "permisoId" AS permiso_id, 
        "nombrePermiso" AS nombre_permiso, 
        "descripcionPermiso" AS descripcion_permiso, 
        "fechaCreacion" AS fecha_creacion, 
        "Permiso"."activo" AS activo, 
        "hashTabla" AS hash_tabla
    FROM "Permiso"
    ORDER BY "permisoId"  -- Ordenar por permisoId
    OFFSET p_skip         -- Saltar los primeros registros según p_skip
    LIMIT p_limit;        -- Limitar la cantidad de registros devueltos
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerPermisosPorNombre"(
    p_nombre_permiso VARCHAR(50)
)
RETURNS TABLE(
    permiso_id INT,
    nombre_permiso VARCHAR(50),
    descripcion_permiso VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT 
        "permisoId" AS permisoId, 
        "nombrePermiso" AS nombrePermiso, 
        "descripcionPermiso" AS descripcionPermiso, 
        "fechaCreacion" AS fechaCreacion, 
        "Permiso"."activo" AS activo, 
        "hashTabla" AS hashTabla
    FROM "Permiso"
    WHERE "nombrePermiso" = p_nombre_permiso;
END;
$$;

CREATE OR REPLACE FUNCTION public."crearPermiso"(
    p_nombre_permiso VARCHAR(50),
    p_descripcion_permiso VARCHAR(100)
)
RETURNS TABLE(
    permiso_id INT,
    nombre_permiso VARCHAR(50),
    descripcion_permiso VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
DECLARE
    temp_permiso_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
BEGIN
    -- verificar si existe un permiso con ese nombre
    IF EXISTS(
        SELECT 1
        FROM "Permiso"
        WHERE "nombrePermiso" = p_nombre_permiso
    ) THEN
        RAISE EXCEPTION 'Ya existe un permiso con el nombre ingresado';
    ELSE 
        INSERT INTO "Permiso"(
            "nombrePermiso",
            "descripcionPermiso",
            "activo",
            "hashTabla"
        ) VALUES(
            p_nombre_permiso,
            p_descripcion_permiso,
            TRUE, -- Activo por defecto
            'HASHDUMP'
        ) RETURNING "permisoId", "fechaCreacion", "hashTabla" INTO temp_permiso_id, temp_fecha_creacion, temp_hash_tabla;
    
    -- agregar hash
    temp_hash_tabla := "calcularHashPermiso"(temp_permiso_id);
    UPDATE "Permiso"
    SET "hashTabla" = temp_hash_tabla
    WHERE "permisoId" = temp_permiso_id;
    
    -- Devolver datos actualizados en snake_case
    RETURN QUERY SELECT 
        temp_permiso_id AS permiso_id, 
        p_nombre_permiso AS nombre_permiso, 
        p_descripcion_permiso AS descripcion_permiso, 
        temp_fecha_creacion AS fecha_creacion, 
        TRUE AS activo, -- Siempre se devuelve activo como TRUE
        temp_hash_tabla AS hash_tabla;
    END IF;
END;
$$;

-- QUEDARIA AGREGAR QUE PRIMERO ELIMNE TODAS LAS TUPLAS EN DONDE ESTA ESE PERMISO EN LA TABLA DE RELACIONES
CREATE OR REPLACE FUNCTION public."eliminarPermiso"(
    p_nombre_permiso VARCHAR(50)
)
RETURNS TABLE (
    permisoId INT,
    nombrePermiso VARCHAR(50),
    descripcionPermiso VARCHAR(100),
    fechaCreacion TIMESTAMP,
    activo BOOLEAN,
    hashTabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
DECLARE
    temp_permiso_id INT;
    temp_id_intermedia INT;
    temp_hash_intermedia VARCHAR(100);
    temp_hash_permiso VARCHAR(100);
    temp_activo BOOLEAN;
BEGIN
    -- Verificar si el permiso existe y si está activo
    SELECT "permisoId", "Permiso"."activo"
    INTO temp_permiso_id, temp_activo
    FROM "Permiso"
    WHERE "nombrePermiso" = p_nombre_permiso;

    -- si no se encontró el permiso, lanzar excepción
    IF NOT FOUND THEN
        RAISE EXCEPTION 'El permiso no existe';
    END IF;

    -- Actualizar el estado del permiso a inactivo (borrado lógico)
    UPDATE "Permiso"
    SET "activo" = FALSE
    WHERE "permisoId" = temp_permiso_id;

    -- Actualizar el hash de la tabla permiso
    temp_hash_permiso := "calcularHashPermiso"(temp_permiso_id);
    UPDATE "Permiso"
    SET "hashTabla" = temp_hash_permiso
    WHERE "permisoId" = temp_permiso_id;

    -- Devolver el permiso 
    RETURN QUERY SELECT 
        temp_permiso_id AS permiso_id, 
        p_nombre_permiso AS nombre_permiso, 
        "descripcionPermiso" AS descripcion_permiso, 
        "fechaCreacion" AS fecha_creacion, 
        FALSE AS activo, -- Siempre se devuelve activo como FALSE
        temp_hash_permiso AS hash_tabla
    
    FROM "Permiso" 
    WHERE "permisoId" = temp_permiso_id;
END;
$$;

