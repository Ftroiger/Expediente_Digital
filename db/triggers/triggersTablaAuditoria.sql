CREATE OR REPLACE TRIGGER triggerDocumentoAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Documento"
FOR EACH ROW
EXECUTE FUNCTION logDocumentoAuditoria();

CREATE OR REPLACE TRIGGER triggerDocumentoXMovimiento
AFTER INSERT OR UPDATE OR DELETE ON "DocumentoXMovimiento"
FOR EACH ROW
EXECUTE FUNCTION logDocumentoXMovimientoAuditoria();

CREATE OR REPLACE TRIGGER triggerEstadoExpedienteAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "EstadoExpediente"
FOR EACH ROW
EXECUTE FUNCTION logEstadoExpedienteAuditoria();

CREATE OR REPLACE TRIGGER triggerExpedienteAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Expediente"
FOR EACH ROW
EXECUTE FUNCTION logExpedienteAuditoria();

CREATE OR REPLACE TRIGGER triggerExpedienteXNormaAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "ExpedienteXNorma"
FOR EACH ROW
EXECUTE FUNCTION logExpedienteXNormaAuditoria();

CREATE OR REPLACE TRIGGER triggerHistorialEstadoExpedienteAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "HistorialEstadoExpediente"
FOR EACH ROW
EXECUTE FUNCTION logHistorialEstadoExpedienteAuditoria();

CREATE OR REPLACE TRIGGER triggerMovimientoAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Movimiento"
FOR EACH ROW 
EXECUTE FUNCTION logMovimientoAuditoria();

CREATE OR REPLACE TRIGGER triggerNormaAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Norma"
FOR EACH ROW
EXECUTE FUNCTION logNormaAuditoria();

CREATE OR REPLACE TRIGGER triggerPermisoAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Permiso"
FOR EACH ROW
EXECUTE FUNCTION logPermisoAuditoria();

CREATE OR REPLACE TRIGGER triggerRolXUsuarioAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "RolXUsuario"
FOR EACH ROW
EXECUTE FUNCTION logRolXUsuarioAuditoria();

CREATE OR REPLACE TRIGGER triggerRolAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Rol"
FOR EACH ROW
EXECUTE FUNCTION logRolAuditoria();

CREATE OR REPLACE TRIGGER triggerRolXPermisoAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "RolXPermiso"
FOR EACH ROW
EXECUTE FUNCTION logRolXPermisoAuditoria();

CREATE OR REPLACE TRIGGER triggerTipoExpedienteAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "TipoExpediente"
FOR EACH ROW
EXECUTE FUNCTION logTipoExpedienteAuditoria();

CREATE OR REPLACE TRIGGER triggerTipoNormaAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "TipoNorma"
FOR EACH ROW
EXECUTE FUNCTION logTipoNormaAuditoria();

CREATE OR REPLACE TRIGGER triggerUsuarioAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Usuario"
FOR EACH ROW
EXECUTE FUNCTION logUsuarioAuditoria();

CREATE OR REPLACE TRIGGER triggerNotificacionAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "Notificacion"
FOR EACH ROW
EXECUTE FUNCTION logNotificacionAuditoria();

CREATE OR REPLACE TRIGGER triggerTipoNotificacionAuditoria
AFTER INSERT OR UPDATE OR DELETE ON "TipoNotificacion"
FOR EACH ROW
EXECUTE FUNCTION logTipoNotificacionAuditoria();