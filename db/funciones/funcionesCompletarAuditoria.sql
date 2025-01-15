

CREATE OR REPLACE FUNCTION "completarRolXPermisoAuditoria"(
 p_rol_x_permiso_id INT,
 p_id_address VARCHAR(20),
 p_host_name VARCHAR(100),
 p_user_agent VARCHAR(100),
 p_usuario_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si rol x permiso id existe en la tabla rol x permiso
    IF NOT EXISTS(SELECT 1 FROM "RolXPermiso" WHERE "rolXPermisoId" = p_rol_x_permiso_id) THEN
        RAISE EXCEPTION 'El rol x permiso Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese rol x permiso Id
    IF NOT EXISTS(SELECT 1 FROM "RolXPermisoAuditoria" where "rolXPermisoId" = p_rol_x_permiso_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese rol x permiso Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de permiso X rol Aplicacion
    UPDATE "RolXPermisoAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id
    WHERE "rolXPermisoId" = p_rol_x_permiso_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarPermisoAuditoria"(
    p_permiso_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si permiso id existe en la tabla permiso
    IF NOT EXISTS(SELECT 1 FROM "Permiso" WHERE "permisoId" = p_permiso_id) THEN
        RAISE EXCEPTION 'El permiso Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese permiso Id
    IF NOT EXISTS(SELECT 1 FROM "PermisoAuditoria" where "permisoId" = p_permiso_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese permiso Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de permiso
    UPDATE "PermisoAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id
    WHERE "permisoId" = p_permiso_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarRolAuditoria"(
    p_rol_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT
) 
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si rol id existe en la tabla rol
    IF NOT EXISTS(SELECT 1 FROM "Rol" WHERE "rolId" = p_rol_id) THEN
        RAISE EXCEPTION 'El rol Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese rol Id
    IF NOT EXISTS(SELECT 1 FROM "RolAuditoria" where "rolId" = p_rol_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese rol Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de rol
    UPDATE "RolAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id
    WHERE "rolId" = p_rol_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarRolXUsuarioAuditoria"(
    p_rol_x_usuario_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si rol x usuario id existe en la tabla rol x usuario
    IF NOT EXISTS(SELECT 1 FROM "RolXUsuario" WHERE "rolXUsuarioId" = p_rol_x_usuario_id) THEN
        RAISE EXCEPTION 'El rol x usuario Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese rol x usuario Id
    IF NOT EXISTS(SELECT 1 FROM "RolXUsuarioAuditoria" where "rolXUsuarioId" = p_rol_x_usuario_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese rol x usuario Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de rol X usuario
    UPDATE "RolXUsuarioAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id
    WHERE "rolXUsuarioId" = p_rol_x_usuario_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarUsuarioAuditoria"(
    p_usuario_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si usuario id existe en la tabla usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_id) THEN
        RAISE EXCEPTION 'El usuario Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese usuario Id
    IF NOT EXISTS(SELECT 1 FROM "UsuarioAuditoria" where "usuarioId" = p_usuario_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese usuario Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de usuario
    UPDATE "UsuarioAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id
    WHERE "usuarioId" = p_usuario_id AND "ipAddress" IS NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarDocumentoAuditoria"(
    p_documento_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN
    --Verificar si la aplicacion id existe para algun usuario 
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si documento id existe en la tabla documento
    IF NOT EXISTS(SELECT 1 FROM "Documento" WHERE "documentoId" = p_documento_id) THEN
        RAISE EXCEPTION 'El documento Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese documento Id
    IF NOT EXISTS(SELECT 1 FROM "DocumentoAuditoria" where "documentoId" = p_documento_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese documento Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de documento
    UPDATE "DocumentoAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "documentoId" = p_documento_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarDocumentoXMovimientoAuditoria"(
    p_documento_x_movimiento_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si documento x movimiento id existe en la tabla documento x movimiento
    IF NOT EXISTS(SELECT 1 FROM "DocumentoXMovimiento" WHERE "documentoXMovimientoId" = p_documento_x_movimiento_id) THEN
        RAISE EXCEPTION 'El documento x movimiento Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese documento x movimiento Id
    IF NOT EXISTS(SELECT 1 FROM "DocumentoXMovimientoAuditoria" where "documentoXMovimientoId" = p_documento_x_movimiento_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese documento x movimiento Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de documento x movimiento
    UPDATE "DocumentoXMovimientoAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "documentoXMovimientoId" = p_documento_x_movimiento_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarEstadoExpedienteAuditoria"(
    p_estado_expediente_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si estado expediente id existe en la tabla estado expediente
    IF NOT EXISTS(SELECT 1 FROM "EstadoExpediente" WHERE "estadoExpedienteId" = p_estado_expediente_id) THEN
        RAISE EXCEPTION 'El estado expediente Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese estado expediente Id
    IF NOT EXISTS(SELECT 1 FROM "EstadoExpedienteAuditoria" where "estadoExpedienteId" = p_estado_expediente_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese estado expediente Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de estado expediente
    UPDATE "EstadoExpedienteAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "estadoExpedienteId" = p_estado_expediente_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarExpedienteAuditoria"(
    p_expediente_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
DECLARE 
    p_historial_estado_expediente_id INT;
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si expediente id existe en la tabla expediente
    IF NOT EXISTS(SELECT 1 FROM "Expediente" WHERE "expedienteId" = p_expediente_id) THEN
        RAISE EXCEPTION 'El expediente Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese expediente Id
    IF NOT EXISTS(SELECT 1 FROM "ExpedienteAuditoria" where "expedienteId" = p_expediente_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese expediente Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de expediente
    UPDATE "ExpedienteAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "expedienteId" = p_expediente_id AND "ipAddress" IS NULL;

    select "historialEstadoExpedienteId" 
    into p_historial_estado_expediente_id 
    from "HistorialEstadoExpediente" 
    where "expedienteId" = p_expediente_id AND "fechaHasta" is NULL order by "fechaDesde" desc limit 1;

    UPDATE "HistorialEstadoExpedienteAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "historialEstadoExpedienteId" = p_historial_estado_expediente_id AND "ipAddress" IS NULL;


END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarExpedienteXNormaAuditoria"(
    p_expediente_x_norma_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si expediente x norma id existe en la tabla expediente x norma
    IF NOT EXISTS(SELECT 1 FROM "ExpedienteXNorma" WHERE "expedienteXNormaId" = p_expediente_x_norma_id) THEN
        RAISE EXCEPTION 'El expediente x norma Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese expediente x norma Id
    IF NOT EXISTS(SELECT 1 FROM "ExpedienteXNormaAuditoria" where "expedienteXNormaId" = p_expediente_x_norma_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese expediente x norma Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de expediente x norma
    UPDATE "ExpedienteXNormaAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "expedienteXNormaId" = p_expediente_x_norma_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarHistorialEstadoExpedienteAuditoria"(
    p_historial_estado_expediente_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
) 
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si historial estado expediente id existe en la tabla historial estado expediente
    IF NOT EXISTS(SELECT 1 FROM "HistorialEstadoExpediente" WHERE "historialEstadoExpedienteId" = p_historial_estado_expediente_id) THEN
        RAISE EXCEPTION 'El historial estado expediente Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese historial estado expediente Id
    IF NOT EXISTS(SELECT 1 FROM "HistorialEstadoExpedienteAuditoria" where "historialEstadoExpedienteId" = p_historial_estado_expediente_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese historial estado expediente Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de historial estado expediente
    UPDATE "HistorialEstadoExpedienteAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "historialEstadoExpedienteId" = p_historial_estado_expediente_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarMovimientoAuditoria"(
    p_movimiento_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si movimiento id existe en la tabla movimiento
    IF NOT EXISTS(SELECT 1 FROM "Movimiento" WHERE "movimientoId" = p_movimiento_id) THEN
        RAISE EXCEPTION 'El movimiento Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese movimiento Id
    IF NOT EXISTS(SELECT 1 FROM "MovimientoAuditoria" where "movimientoId" = p_movimiento_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese movimiento Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de movimiento
    UPDATE "MovimientoAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "movimientoId" = p_movimiento_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarNormaAuditoria"(
    p_norma_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si norma id existe en la tabla norma
    IF NOT EXISTS(SELECT 1 FROM "Norma" WHERE "normaId" = p_norma_id) THEN
        RAISE EXCEPTION 'El norma Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese norma Id
    IF NOT EXISTS(SELECT 1 FROM "NormaAuditoria" where "normaId" = p_norma_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese norma Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de norma
    UPDATE "NormaAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "normaId" = p_norma_id AND "ipAddress" IS NULL;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION "completarTipoExpedienteAuditoria"(
    p_tipo_expediente_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si tipo expediente id existe en la tabla tipo expediente
    IF NOT EXISTS(SELECT 1 FROM "TipoExpediente" WHERE "tipoExpedienteId" = p_tipo_expediente_id) THEN
        RAISE EXCEPTION 'El tipo expediente Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese tipo expediente Id
    IF NOT EXISTS(SELECT 1 FROM "TipoExpedienteAuditoria" where "tipoExpedienteId" = p_tipo_expediente_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese tipo expediente Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de tipo expediente
    UPDATE "TipoExpedienteAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "tipoExpedienteId" = p_tipo_expediente_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarTipoNormaAuditoria"(
    p_tipo_norma_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    --Verificar si la aplicacion id existe para algun usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_aplicacion_responsable_id) THEN
        RAISE EXCEPTION 'La usuarioId no pertenece a ningun Usuario';
    END IF;
    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si tipo norma id existe en la tabla tipo norma
    IF NOT EXISTS(SELECT 1 FROM "TipoNorma" WHERE "tipoNormaId" = p_tipo_norma_id) THEN
        RAISE EXCEPTION 'El tipo norma Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese tipo norma Id
    IF NOT EXISTS(SELECT 1 FROM "TipoNormaAuditoria" where "tipoNormaId" = p_tipo_norma_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese tipo norma Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de tipo norma
    UPDATE "TipoNormaAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "tipoNormaId" = p_tipo_norma_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarNotificacionAuditoria"(
    p_notificacion_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si notificacion id existe en la tabla notificacion
    IF NOT EXISTS(SELECT 1 FROM "Notificacion" WHERE "notificacionId" = p_notificacion_id) THEN
        RAISE EXCEPTION 'El notificacion Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese notificacion Id
    IF NOT EXISTS(SELECT 1 FROM "NotificacionAuditoria" where "notificacionId" = p_notificacion_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese notificacion Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de notificacion
    UPDATE "NotificacionAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id
    WHERE "notificacionId" = p_notificacion_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarTipoNotificacionAuditoria"(
    p_tipo_notificacion_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si tipo notificacion id existe en la tabla tipo notificacion
    IF NOT EXISTS(SELECT 1 FROM "TipoNotificacion" WHERE "tipoNotificacionId" = p_tipo_notificacion_id) THEN
        RAISE EXCEPTION 'El tipo notificacion Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese tipo notificacion Id
    IF NOT EXISTS(SELECT 1 FROM "TipoNotificacionAuditoria" where "tipoNotificacionId" = p_tipo_notificacion_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese tipo notificacion Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de tipo notificacion
    UPDATE "TipoNotificacionAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "tipoNotificacionId" = p_tipo_notificacion_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarUsuarioGatewayAuditoria"(
    p_usuario_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si usuario id existe en la tabla usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_id) THEN
        RAISE EXCEPTION 'El usuario Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese usuario Id
    IF NOT EXISTS(SELECT 1 FROM "UsuarioAuditoria" where "usuarioId" = p_usuario_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese usuario Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de usuario
    UPDATE "UsuarioAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "usuarioId" = p_usuario_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION "completarRolXUsuarioGatewayAuditoria"(
    p_usuario_id INT,
    p_id_address VARCHAR(20),
    p_host_name VARCHAR(100),
    p_user_agent VARCHAR(100),
    p_usuario_responsable_id INT,
    p_usuario_aplicacion_responsable_id INT
)
RETURNS void AS
$$
BEGIN

    -- Verificar si el usuario responsable Id existe en la tabla de usuarios
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_responsable_id) THEN
        RAISE EXCEPTION 'El usuario responsable no existe en la tabla de usuarios';
    END IF;
    -- Verificar si usuario id existe en la tabla usuario
    IF NOT EXISTS(SELECT 1 FROM "Usuario" WHERE "usuarioId" = p_usuario_id) THEN
        RAISE EXCEPTION 'El usuario Id no existe';
    END IF;
    -- Verificar si exite el tupla de auditoria con ese usuario Id
    IF NOT EXISTS(SELECT 1 FROM "UsuarioAuditoria" where "usuarioId" = p_usuario_id) THEN
        RAISE EXCEPTION 'El registro de auditoria con ese usuario Id no existe';
    END IF;
    -- Actualiza el registro de auditoria de usuario
    UPDATE "RolXUsuarioAuditoria"
    SET "ipAddress" = p_id_address,
        "hostName" = p_host_name,
        "userAgent" = p_user_agent,
        "usuarioResponsableId" = p_usuario_responsable_id,
        "usuarioAplicacionResponsableId" = p_usuario_aplicacion_responsable_id
    WHERE "usuarioId" = p_usuario_id AND "ipAddress" IS NULL;

END;
$$ LANGUAGE plpgsql;