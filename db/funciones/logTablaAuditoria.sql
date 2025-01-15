CREATE OR REPLACE FUNCTION logDocumentoAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "DocumentoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "documentoId",
            "firmaDigitalId",
            "cddId",
            "nombreArchivo",
            "tipoDocumento",
            "versionDocumento",
            "cantPaginas",
            "fechaCreacion",
            "hashTabla",
            "firmado",
            "estado",
            "activo",
            "documentoOrigenId",
            "qrId"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."documentoId",
            NEW."firmaDigitalId",
            NEW."cddId",
            NEW."nombreArchivo",
            NEW."tipoDocumento",
            NEW."versionDocumento",
            NEW."cantPaginas",
            NEW."fechaCreacion",
            NEW."hashTabla",
            NEW."firmado",
            NEW."estado",
            NEW."activo",
            NEW."documentoOrigenId",
            NEW."qrId"
        );
    ELSE
        INSERT INTO "DocumentoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "documentoId",
            "firmaDigitalId",
            "cddId",
            "nombreArchivo",
            "tipoDocumento",
            "versionDocumento",
            "cantPaginas",
            "fechaCreacion",
            "hashTabla",
            "firmado",
            "estado",
            "activo",
            "documentoOrigenId",
            "qrId"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."documentoId",
            OLD."firmaDigitalId",
            OLD."cddId",
            OLD."nombreArchivo",
            OLD."tipoDocumento",
            OLD."versionDocumento",
            OLD."cantPaginas",
            OLD."fechaCreacion",
            OLD."hashTabla",
            OLD."firmado",
            OLD."estado",
            OLD."activo",
            OLD."documentoOrigenId",
            OLD."qrId"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logDocumentoXMovimientoAuditoria()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "DocumentoXMovimientoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "documentoXMovimientoId",
            "movimientoId",
            "documentoId",
            "fechaAsociacion",
            "foliosInicial",
            "foliosFinal",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."documentoXMovimientoId",
            NEW."movimientoId",
            NEW."documentoId",
            NEW."fechaAsociacion",
            NEW."foliosInicial",
            NEW."foliosFinal",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "DocumentoXMovimientoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "documentoXMovimientoId",
            "movimientoId",
            "documentoId",
            "fechaAsociacion",
            "foliosInicial",
            "foliosFinal",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."documentoXMovimientoId",
            OLD."movimientoId",
            OLD."documentoId",
            OLD."fechaAsociacion",
            OLD."foliosInicial",
            OLD."foliosFinal",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END; 
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logEstadoExpedienteAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "EstadoExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "estadoExpedienteId",
            "nombreEstadoExpediente",
            "descripcionEstadoExpediente",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."estadoExpedienteId",
            NEW."nombreEstadoExpediente",
            NEW."descripcionEstadoExpediente",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "EstadoExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "estadoExpedienteId",
            "nombreEstadoExpediente",
            "descripcionEstadoExpediente",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."estadoExpedienteId",
            OLD."nombreEstadoExpediente",
            OLD."descripcionEstadoExpediente",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logExpedienteAuditoria()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP='INSERT' THEN
        INSERT INTO "ExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "expedienteId",
            "tipoExpedienteId",
            "numeroExpediente",
            "areaIniciadoraId",
            "usuarioCreadorFisicoId",
            "usuarioCreadorAplicacionId",
            "asuntoExpediente",
            "fechaCreacion",
            "fechaUltimoMovimiento",
            "visibilidadExpediente",
            "activo",
            "hashTabla",
            "temaNombre",
            "areaActualidadId",
            "foliosApertura",
            "foliosActuales",
            "documentoSiradId"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."expedienteId",
            NEW."tipoExpedienteId",
            NEW."numeroExpediente",
            NEW."areaIniciadoraId",
            NEW."usuarioCreadorFisicoId",
            NEW."usuarioCreadorAplicacionId",
            NEW."asuntoExpediente",
            NEW."fechaCreacion",
            NEW."fechaUltimoMovimiento",
            NEW."visibilidadExpediente",
            NEW."activo",
            NEW."hashTabla",
            NEW."temaNombre",
            NEW."areaActualidadId",
            NEW."foliosApertura",
            NEW."foliosActuales",
            NEW."documentoSiradId"
        );
    ELSE
    INSERT INTO "ExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "expedienteId",
            "tipoExpedienteId",
            "numeroExpediente",
            "areaIniciadoraId",
            "usuarioCreadorFisicoId",
            "usuarioCreadorAplicacionId",
            "asuntoExpediente",
            "fechaCreacion",
            "fechaUltimoMovimiento",
            "visibilidadExpediente",
            "activo",
            "hashTabla",
            "temaNombre",
            "areaActualidadId",
            "foliosApertura",
            "foliosActuales",
            "documentoSiradId"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."expedienteId",
            OLD."tipoExpedienteId",
            OLD."numeroExpediente",
            OLD."areaIniciadoraId",
            OLD."usuarioCreadorFisicoId",
            OLD."usuarioCreadorAplicacionId",
            OLD."asuntoExpediente",
            OLD."fechaCreacion",
            OLD."fechaUltimoMovimiento",
            OLD."visibilidadExpediente",
            OLD."activo",
            OLD."hashTabla",
            OLD."temaNombre",
            OLD."areaActualidadId",
            OLD."foliosApertura",
            OLD."foliosActuales",
            OLD."documentoSiradId"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logExpedienteXNormaAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "ExpedienteXNormaAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "expedienteXNormaId",
            "fechaAsociacion",
            "hashTabla",
            "activo",
            "normaId",
            "expedienteId"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."expedienteXNormaId",
            NEW."fechaAsociacion",
            NEW."hashTabla",
            NEW."activo",
            NEW."normaId",
            NEW."expedienteId"
        );
    ELSE
        INSERT INTO "ExpedienteXNormaAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "expedienteXNormaId",
            "fechaAsociacion",
            "hashTabla",
            "activo",
            "normaId",
            "expedienteId"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."expedienteXNormaId",
            OLD."fechaAsociacion",
            OLD."hashTabla",
            OLD."activo",
            OLD."normaId",
            OLD."expedienteId"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logHistorialEstadoExpedienteAuditoria()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "HistorialEstadoExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "historialEstadoExpedienteId",
            "estadoExpedienteId",
            "expedienteId",
            "fechaDesde",
            "fechaHasta",
            "hashTabla",
            "activo"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."historialEstadoExpedienteId",
            NEW."estadoExpedienteId",
            NEW."expedienteId",
            NEW."fechaDesde",
            NEW."fechaHasta",
            NEW."hashTabla",
            NEW."activo"
        );
    ELSE
        INSERT INTO "HistorialEstadoExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "historialEstadoExpedienteId",
            "estadoExpedienteId",
            "expedienteId",
            "fechaDesde",
            "fechaHasta",
            "hashTabla",
            "activo"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."historialEstadoExpedienteId",
            OLD."estadoExpedienteId",
            OLD."expedienteId",
            OLD."fechaDesde",
            OLD."fechaHasta",
            OLD."hashTabla",
            OLD."activo"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION logMovimientoAuditoria()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "MovimientoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "movimientoId",
            "tramiteId",
            "expedienteId",
            "usuarioFisicoId",
            "usuarioAplicacionId",
            "areaOrigenId",
            
            "areaDestinoId",
            "fechaCreacion",
            "observacionMovimiento",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."movimientoId",
            NEW."tramiteId",
            NEW."expedienteId",
            NEW."usuarioFisicoId",
            NEW."usuarioAplicacionId",
            NEW."areaOrigenId",
            NEW."areaDestinoId",
            NEW."fechaCreacion",
            NEW."observacionMovimiento",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "MovimientoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "movimientoId",
            "tramiteId",
            "expedienteId",
            "usuarioFisicoId",
            "usuarioAplicacionId",
            "areaOrigenId",
            "areaDestinoId",
            "fechaCreacion",
            "observacionMovimiento",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."movimientoId",
            OLD."tramiteId",
            OLD."expedienteId",
            OLD."usuarioFisicoId",
            OLD."usuarioAplicacionId",
            OLD."areaOrigenId",
            OLD."areaDestinoId",
            OLD."fechaCreacion",
            OLD."observacionMovimiento",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logNormaAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "NormaAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "normaId",
            "tipoNormaId",
            "numeroNorma",
            "descripcionNorma",
            "fechaCreacion",
            "normaCddId",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."normaId",
            NEW."tipoNormaId",
            NEW."numeroNorma",
            NEW."descripcionNorma",
            NEW."fechaCreacion",
            NEW."normaCddId",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "NormaAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "normaId",
            "tipoNormaId",
            "numeroNorma",
            "descripcionNorma",
            "fechaCreacion",
            "normaCddId",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."normaId",
            OLD."tipoNormaId",
            OLD."numeroNorma",
            OLD."descripcionNorma",
            OLD."fechaCreacion",
            OLD."normaCddId",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logPermisoAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "PermisoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "permisoId",
            "nombrePermiso",
            "descripcionPermiso",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."permisoId",
            NEW."nombrePermiso",
            NEW."descripcionPermiso",
            NEW."fechaCreacion",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "PermisoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "permisoId",
            "nombrePermiso",
            "descripcionPermiso",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."permisoId",
            OLD."nombrePermiso",
            OLD."descripcionPermiso",
            OLD."fechaCreacion",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION logRolXUsuarioAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "RolXUsuarioAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "rolXUsuarioId",
            "usuarioId",
            "rolId",
            "fechaCreacion",
            "activo",
            "hashTabla"
        ) VALUES (
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."rolXUsuarioId",
            NEW."usuarioId",
            NEW."rolId",
            NEW."fechaCreacion",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "RolXUsuarioAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "rolXUsuarioId",
            "usuarioId",
            "rolId",
            "fechaCreacion",
            "activo",
            "hashTabla"
        ) VALUES (
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."rolXUsuarioId",
            OLD."usuarioId",
            OLD."rolId",
            OLD."fechaCreacion",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION logRolAuditoria()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "RolAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "rolId",
            "nombreRol",
            "descripcionRol",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."rolId",
            NEW."nombreRol",
            NEW."descripcionRol",
            NEW."fechaCreacion",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE 
        INSERT INTO "RolAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "rolId",
            "nombreRol",
            "descripcionRol",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."rolId",
            OLD."nombreRol",
            OLD."descripcionRol",
            OLD."fechaCreacion",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logRolXPermisoauditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "RolXPermisoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "rolXPermisoId",
            "permisoId",
            "rolId",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."rolXPermisoId",
            NEW."permisoId",
            NEW."rolId",
            NEW."fechaCreacion",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "RolXPermisoAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "rolXPermisoId",
            "permisoId",
            "rolId",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."rolXPermisoId",
            OLD."permisoId",
            OLD."rolId",
            OLD."fechaCreacion",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logTipoExpedienteAuditoria()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'INSERT' THEN 
        INSERT INTO "TipoExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "tipoExpedienteId",
            "nombreTipoExpediente",
            "descripcionTipoExpediente",
            "activo",
            "hashTabla"
        ) 
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."tipoExpedienteId",
            NEW."nombreTipoExpediente",
            NEW."descripcionTipoExpediente",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "TipoExpedienteAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "tipoExpedienteId",
            "nombreTipoExpediente",
            "descripcionTipoExpediente",
            "activo",
            "hashTabla"
        ) 
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."tipoExpedienteId",
            OLD."nombreTipoExpediente",
            OLD."descripcionTipoExpediente",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logTipoNormaAuditoria()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "TipoNormaAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "tipoNormaId",
            "nombreTipoNorma",
            "descripcionTipoNorma",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."tipoNormaId",
            NEW."nombreTipoNorma",
            NEW."descripcionTipoNorma",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "TipoNormaAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "tipoNormaId",
            "nombreTipoNorma",
            "descripcionTipoNorma",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."tipoNormaId",
            OLD."nombreTipoNorma",
            OLD."descripcionTipoNorma",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF; 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logUsuarioAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "UsuarioAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "usuarioId",
            "cuilUsuario",
            "nombreUsuario",
            "fechaCreacion",
            "fechaBaja",
            "areaId",
            "aplicacionVediId",
            "apiKey",
            "usuarioAlta",
            "activo",
            "hashTabla"
        ) VALUES (
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."usuarioId",
            NEW."cuilUsuario",
            NEW."nombreUsuario",
            NEW."fechaCreacion",
            NEW."fechaBaja",
            NEW."areaId",
            NEW."aplicacionVediId",
            NEW."apiKey",
            NEW."usuarioAlta",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "UsuarioAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "usuarioId",
            "cuilUsuario",
            "nombreUsuario",
            "fechaCreacion",
            "fechaBaja",
            "areaId",
            "aplicacionVediId",
            "apiKey",
            "usuarioAlta",
            "activo",
            "hashTabla"
        ) VALUES (
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."usuarioId",
            OLD."cuilUsuario",
            OLD."nombreUsuario",
            OLD."fechaCreacion",
            OLD."fechaBaja",
            OLD."areaId",
            OLD."aplicacionVediId",
            OLD."apiKey",
            OLD."usuarioAlta",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logNotificacionAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "NotificacionAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "notificacionId",
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
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."notificacionId",
            NEW."usuarioNotificadoId",
            NEW."tipoNotificacionId",
            NEW."descripcionNotificacion",
            NEW."usuarioAfectadoId",
            NEW."leido",
            NEW."fechaCreacion",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "NotificacionAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "notificacionId",
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
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."notificacionId",
            OLD."usuarioNotificadoId",
            OLD."tipoNotificacionId",
            OLD."descripcionNotificacion",
            OLD."usuarioAfectadoId",
            OLD."leido",
            OLD."fechaCreacion",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION logTipoNotificacionAuditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO "TipoNotificacionAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "tipoNotificacionId",
            "nombreTipoNotificacion",
            "descripcionTipoNotificacion",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            NEW."tipoNotificacionId",
            NEW."nombreTipoNotificacion",
            NEW."descripcionTipoNotificacion",
            NEW."fechaCreacion",
            NEW."activo",
            NEW."hashTabla"
        );
    ELSE
        INSERT INTO "TipoNotificacionAuditoria"(
            "fechaModificacion",
            "operacionRealizada",
            "tipoNotificacionId",
            "nombreTipoNotificacion",
            "descripcionTipoNotificacion",
            "fechaCreacion",
            "activo",
            "hashTabla"
        )
        VALUES(
            CURRENT_TIMESTAMP,
            TG_OP,
            OLD."tipoNotificacionId",
            OLD."nombreTipoNotificacion",
            OLD."descripcionTipoNotificacion",
            OLD."fechaCreacion",
            OLD."activo",
            OLD."hashTabla"
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;