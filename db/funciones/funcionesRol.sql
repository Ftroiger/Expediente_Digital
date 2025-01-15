CREATE OR REPLACE FUNCTION public."crearRol"(
    p_nombre_rol VARCHAR(50),
    p_descripcion_rol VARCHAR(100)
)
RETURNS TABLE(
    rol_id INT,
    nombre_rol VARCHAR(50),
    descripcion_rol VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
DECLARE
    temp_rol_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_hash_tabla VARCHAR(100);
BEGIN
    -- Verificar si el rol ya existe
    IF EXISTS (
        SELECT 1
        FROM "Rol"
        WHERE "nombreRol" = p_nombre_rol
    ) THEN
        RAISE EXCEPTION 'El rol ya existe';
    ELSE
        INSERT INTO "Rol"(
            "nombreRol",
            "descripcionRol",
            "activo",
            "hashTabla"
        ) VALUES (
            p_nombre_rol,
            p_descripcion_rol,
            TRUE,
            'HASHDUMP'
        ) RETURNING "rolId", "fechaCreacion", "hashTabla" INTO temp_rol_id, temp_fecha_creacion, temp_hash_tabla;

    -- agregar hash
    temp_hash_tabla := "calcularHashRol"(temp_rol_id);
    UPDATE "Rol"
    SET "hashTabla" = temp_hash_tabla
    WHERE "rolId" = temp_rol_id;

    -- devolver datos actualizados
    RETURN QUERY SELECT
        temp_rol_id AS rol_id,
        p_nombre_rol AS nombre_rol,
        p_descripcion_rol AS descripcion_rol,
        temp_fecha_creacion AS fecha_creacion,
        TRUE AS activo,
        temp_hash_tabla AS hash_tabla;
    END IF;
END;
$$;
        
CREATE OR REPLACE FUNCTION public."obtenerRoles"(
    p_skip INT,
    p_limit INT
)
RETURNS TABLE(
    rol_id INT,
    nombre_rol VARCHAR(50),
    descripcion_rol VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT
        "rolId" AS rol_id,
        "nombreRol" AS nombre_rol,
        "descripcionRol" AS descripcion_rol,
        "fechaCreacion" AS fecha_creacion,
        "Rol"."activo" AS activo,
        "hashTabla" AS hash_tabla
    FROM "Rol"
    LIMIT p_limit
    OFFSET p_skip;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerRolPorId"(
    p_rol_id INT
)
RETURNS TABLE(
    rol_id INT,
    nombre_rol VARCHAR(50),
    descripcion_rol VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT
        "rolId" AS rol_id,
        "nombreRol" AS nombre_rol,
        "descripcionRol" AS descripcion_rol,
        "fechaCreacion" AS fecha_creacion,
        "Rol"."activo" AS activo,
        "hashTabla" AS hash_tabla
    FROM "Rol"
    WHERE "rolId" = p_rol_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe un rol con el id %', p_rol_id;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerRolPorNombre"(
    p_nombre_rol VARCHAR(50)
)
RETURNS TABLE(
    rol_id INT,
    nombre_rol VARCHAR(50),
    descripcion_rol VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT
        "rolId" AS rol_id,
        "nombreRol" AS nombre_rol,
        "descripcionRol" AS descripcion_rol,
        "fechaCreacion" AS fecha_creacion,
        "Rol"."activo" AS activo,
        "hashTabla" AS hash_tabla
    FROM "Rol"
    WHERE "nombreRol" = p_nombre_rol;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe un rol con el nombre %', p_nombre_rol;
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION public."eliminarRolPorNombre"(
    p_nombre_rol VARCHAR(50)
)
RETURNS TABLE(
    rol_id INT,
    nombre_rol VARCHAR(50),
    descripcion_rol VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)LANGUAGE plpgsql
AS $$
DECLARE
    temp_rol_id INT;
    temp_id_intermedia INT;
    temp_hash VARCHAR(100);
    temp_hash_intermedia VARCHAR(100);
    temp_activo BOOLEAN;
BEGIN
    -- Verificar si el rol existe y si está activo
    SELECT "rolId", "Rol"."activo"
    INTO temp_rol_id, temp_activo
    FROM "Rol"
    WHERE "nombreRol" = p_nombre_rol;

    -- Si no se encontró el rol, lanzar excepción
    IF NOT FOUND THEN 
        RAISE EXCEPTION 'No existe un rol con el nombre "%"', p_nombre_rol;
    END IF;

    IF EXISTS (
        SELECT 1
        FROM "RolXUsuario"
        WHERE "rolId" = temp_rol_id
    ) THEN
        RAISE EXCEPTION 'No se puede eliminar el rol "%", ya que tiene usuarios asociados', p_nombre_rol;
    END IF;
    
    -- Actualizar estado a inactivo en la tabla Rol
    UPDATE "Rol"
    SET "activo" = FALSE
    WHERE "rolId" = temp_rol_id;
    
    -- Actualizar hash tabla
    temp_hash := "calcularHashRol"(temp_rol_id);
    UPDATE "Rol"
    SET "hashTabla" = temp_hash
    WHERE "rolId" = temp_rol_id;

    RETURN QUERY SELECT
        "rolId" AS rol_id,
        "nombreRol" AS nombre_rol,
        "descripcionRol" AS descripcion_rol,
        "fechaCreacion" AS fecha_creacion,
        "Rol"."activo",
        "hashTabla" AS hash_tabla
    FROM "Rol"
    WHERE "rolId" = temp_rol_id;
END;
$$;


CREATE OR REPLACE FUNCTION public."obtenerRolesPorNombrePermiso"(
    p_nombre_permiso VARCHAR(50)
)
RETURNS TABLE(
    rol_id INT,
    nombre_rol VARCHAR(50),
    descripcion_rol VARCHAR(100),
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT
        "Rol"."rolId" AS rol_id,
        "Rol"."nombreRol" AS nombre_rol,
        "Rol"."descripcionRol" AS descripcion_rol,
        "Rol"."fechaCreacion" AS fecha_creacion,
        "Rol"."activo" AS activo,
        "Rol"."hashTabla" AS hash_tabla
    FROM "Rol"
    JOIN "RolXPermiso" ON "Rol"."rolId" = "RolXPermiso"."rolId"
    JOIN "Permiso" ON "RolXPermiso"."permisoId" = "Permiso"."permisoId"
    WHERE "Permiso"."nombrePermiso" = p_nombre_permiso;
END;
$$;