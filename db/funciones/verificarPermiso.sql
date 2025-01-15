/* Función para verificar el permiso del usuario aplicacion

    Parámetros:
        p_usuarioAplicacionId INT
        p_accion VARCHAR(100)

    Retorna:
        permiso BOOLEAN

 */
 CREATE OR REPLACE FUNCTION "verificarPermiso"(
    p_usuarioAplicacion_id INT,
    p_accion VARCHAR(100)
 ) RETURNS BOOLEAN AS $$
 DECLARE
    permiso_id INT;
    permiso BOOLEAN;
BEGIN
    -- Buscar el permisoId con la acción deseada
    SELECT "permisoId" INTO permiso_id
    FROM "Permiso"
    WHERE "nombrePermiso" = p_accion;

    -- Si el permiso no existe, devolver un error
    IF permiso_id IS NULL THEN
        RAISE EXCEPTION 'No existe un permiso con la acción %', p_accion;
    END IF;

    -- Verificar si el usuario tiene el permiso
    SELECT EXISTS (
        SELECT 1
        FROM "PermisoXUsuarioAplicacion"
        WHERE "usuarioAplicacionId" = p_usuarioAplicacion_id
        AND "permisoId" = permiso_id
    ) INTO permiso;

    RETURN permiso;
END;
$$ LANGUAGE plpgsql;


/*
    Función para verificar el permiso del usuario con usuarioID

    Parámetros:
        p_usuarioId INT
        p_accion VARCHAR(100)

    Retorna:
        permiso BOOLEAN
*/
CREATE OR REPLACE FUNCTION "verificarPermisoUsuario"(
    p_usuario_id INT,
    p_accion VARCHAR(100)
) RETURNS BOOLEAN AS $$
DECLARE
    permiso_id INT;
    rol_id INT;
    permiso BOOLEAN;
BEGIN
    -- Buscar el permisoId con la acción deseada
    SELECT "permisoId" INTO permiso_id
    FROM "Permiso"
    WHERE "nombrePermiso" = p_accion;

    -- Si el permiso no existe, devolver un error
    IF permiso_id IS NULL THEN
        RAISE EXCEPTION 'No existe un permiso con la acción %', p_accion;
    END IF;

    -- Averiguar si el usuario existe
    IF NOT EXISTS (
        SELECT 1
        FROM "Usuario"
        WHERE "usuarioId" = p_usuario_id
    ) THEN
        RAISE EXCEPTION 'No existe un usuario con el ID %', p_usuario_id;
    END IF;

    -- Verificar el rol del usuario en tabla rol
    SELECT "rolId" INTO rol_id
    FROM "RolXUsuario"
    WHERE "usuarioId" = p_usuario_id;

    -- Si el usuario no tiene rol, devolver un error
    IF rol_id IS NULL THEN
        RAISE EXCEPTION 'El usuario con ID % no tiene un rol asignado', p_usuario_id;
    END IF;

    -- Verificar si el usuario tiene el permiso
    SELECT EXISTS (
        SELECT 1
        FROM "RolXPermiso"
        WHERE "rolId" = rol_id
        AND "permisoId" = permiso_id
    ) INTO permiso;

    RETURN permiso;
END;
$$ LANGUAGE plpgsql;
