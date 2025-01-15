
CREATE OR REPLACE FUNCTION public."asignarRolAUsuario"(
    p_usuario_id INT,
    p_nombre_rol VARCHAR(50)
)
RETURNS TABLE (
    rol_x_usuario_id INT,
    rol_id INT,
    usuario_id INT,
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) 
LANGUAGE plpgsql AS $$
DECLARE
    temp_hash_tabla VARCHAR(100);
    temp_rol_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_rol_x_usuario_id INT;
BEGIN

    -- Verificar que el usuario no tenga rol Asignado
    IF NOT EXISTS(
        SELECT 1
        FROM "RolXUsuario"
        WHERE "usuarioId" = p_usuario_id
    ) THEN
        RAISE EXCEPTION 'El usuario no tiene un rol asignado';
    END IF;
    
    -- Verificar que el rol exista
    IF NOT EXISTS(
        SELECT 1
        FROM "Rol"
        WHERE "nombreRol" = p_nombre_rol
    ) THEN
        RAISE EXCEPTION 'El rol no existe';
    END IF;

    -- Obtener rolId de Usuario Fisico
    temp_rol_id := (SELECT "rolId" FROM "Rol" WHERE "nombreRol" = p_nombre_rol);

    -- Insertar en la tabla intermedia RolXUsuario el nuevo rol de Usuario Fisico
    INSERT INTO "RolXUsuario" ("rolId", "usuarioId", "activo", "hashTabla")
    VALUES (temp_rol_id, p_usuario_id, TRUE, 'HASHDUMP')
    RETURNING "rolXUsuarioId", "fechaCreacion" INTO temp_rol_x_usuario_id, temp_fecha_creacion;

    -- Calcular el hash de la tabla
    temp_hash_tabla := "calcularHashRolXUsuario"(temp_rol_x_usuario_id);
    UPDATE "RolXUsuario"
    SET
        "hashTabla" = temp_hash_tabla
    WHERE
        "rolXUsuarioId" = temp_rol_x_usuario_id;
    
    RETURN QUERY 
    SELECT
        temp_rol_x_usuario_id AS rol_x_usuario_id,
        temp_rol_id AS rol_id,
        p_usuario_id AS usuario_id,
        temp_fecha_creacion AS fecha_creacion,
        TRUE AS activo,
        temp_hash_tabla AS hash_tabla;
END;
$$;



CREATE OR REPLACE FUNCTION public."eliminarRolXUsuarioPorRolId"(
    p_rol_id INT
)
RETURNS TABLE (
    rol_x_usuario_id INT,
    rol_id INT,
    usuario_id INT,
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) 
LANGUAGE plpgsql
AS $$
DECLARE
    temp_rol_x_usuario RECORD;
BEGIN
    -- Verificar si existe la relación
    IF NOT EXISTS(
        SELECT 1
        FROM "RolXUsuario"
        WHERE "rolId" = p_rol_id
    ) THEN
        RAISE EXCEPTION 'La relación entre el rol y el usuario no existe';
    END IF;

    -- Actualizar estado a inactivo en la tabla RolXUsuario para las relaciones con el rol
    FOR temp_rol_x_usuario IN
        UPDATE "RolXUsuario"
        SET "activo" = FALSE
        WHERE "rolId" = p_rol_id
        RETURNING "rolXUsuarioId", "rolId", "usuarioId", "fechaCreacion", "RolXUsuario"."activo"
    LOOP
        -- Actualizar el hash para cada tupla modificada
        UPDATE "RolXUsuario"
        SET "hashTabla" = "calcularHashRolXUsuario"(temp_rol_x_usuario."rolXUsuarioId")
        WHERE "rolXUsuarioId" = temp_rol_x_usuario."rolXUsuarioId";

        -- Devolver las filas modificadas, guardando los resultados
        RETURN QUERY 
        SELECT temp_rol_x_usuario."rolXUsuarioId" AS rol_x_usuario_id, 
               temp_rol_x_usuario."rolId" AS rol_id, 
               temp_rol_x_usuario."usuarioId" AS usuario_id, 
               temp_rol_x_usuario."fechaCreacion" AS fecha_creacion, 
               temp_rol_x_usuario."activo" as activo, 
               "calcularHashRolXUsuario"(temp_rol_x_usuario."rolXUsuarioId") AS hash_tabla;
    END LOOP;

END;
$$;

CREATE OR REPLACE FUNCTION public."eliminarRolXUsuarioPorUsuarioId"(
    p_usuario_id INT
)
RETURNS TABLE (
    rol_x_usuario_id INT,
    rol_id INT,
    usuario_id INT,
    fecha_creacion TIMESTAMP,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
) 
LANGUAGE plpgsql
AS $$
DECLARE
    temp_rol_x_usuario RECORD;
BEGIN
    -- Verificar si existe la relación
    IF NOT EXISTS(
        SELECT 1
        FROM "RolXUsuario"
        WHERE "usuarioId" = p_usuario_id
    ) THEN
        RAISE EXCEPTION 'La relación entre el usuario y el rol no existe';
    END IF;

    -- Actualizar estado a inactivo en la tabla RolXUsuario para las relaciones con el usuario
    FOR temp_rol_x_usuario IN
        UPDATE "RolXUsuario"
        SET "activo" = FALSE
        WHERE "usuarioId" = p_usuario_id
        RETURNING "rolXUsuarioId", "rolId", "usuarioId", "fechaCreacion", "RolXUsuario"."activo"
    LOOP
        -- Actualizar el hash para cada tupla modificada
        UPDATE "RolXUsuario"
        SET "hashTabla" = "calcularHashRolXUsuario"(temp_rol_x_usuario."rolXUsuarioId")
        WHERE "rolXUsuarioId" = temp_rol_x_usuario."rolXUsuarioId";

        -- Devolver las filas modificadas, guardando los resultados
        RETURN QUERY 
        SELECT 
            temp_rol_x_usuario."rolXUsuarioId" AS rol_x_usuario_id, 
            temp_rol_x_usuario."rolId" AS rol_id, 
            temp_rol_x_usuario."usuarioId" AS usuario_id, 
            temp_rol_x_usuario."fechaCreacion" AS fecha_creacion, 
            temp_rol_x_usuario."activo" AS activo, 
            "calcularHashRolXUsuario"(temp_rol_x_usuario."rolXUsuarioId") AS hash_tabla;
    END LOOP;

END;
$$;