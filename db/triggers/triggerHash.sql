CREATE TRIGGER "triggerHashTipoNorma"
BEFORE INSERT OR UPDATE ON "TipoNorma"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashTipoNorma"();

CREATE TRIGGER "triggerHashTipoExpediente"
BEFORE INSERT OR UPDATE ON "TipoExpediente"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashTipoExpediente"();

CREATE TRIGGER "triggerHashPermiso"
BEFORE INSERT OR UPDATE ON "Permiso"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashPermiso"();

CREATE TRIGGER "triggerHashNorma"
BEFORE INSERT OR UPDATE ON "Norma"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashNorma"();

CREATE TRIGGER "triggerHashMovimiento"
BEFORE INSERT OR UPDATE ON "Movimiento"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashMovimiento"();

CREATE TRIGGER "triggerHashHistorialEstadoExpediente"
BEFORE INSERT OR UPDATE ON "HistorialEstadoExpediente"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashHistorialEstadoExpediente"();

CREATE TRIGGER "triggerHashExpedienteXNorma"
BEFORE INSERT OR UPDATE ON "ExpedienteXNorma"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashExpedienteXNorma"();

CREATE TRIGGER "triggerHashExpediente"
BEFORE INSERT OR UPDATE ON "Expediente"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashExpediente"();

CREATE TRIGGER "triggerHashEstadoExpediente"
BEFORE INSERT OR UPDATE ON "EstadoExpediente"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashEstadoExpediente"();

CREATE TRIGGER "triggerHashDocumentoXMovimiento"
BEFORE INSERT OR UPDATE ON "DocumentoXMovimiento"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashDocumentoXMovimiento"();

CREATE TRIGGER "triggerHashDocumento"
BEFORE INSERT OR UPDATE ON "Documento"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashDocumento"();



CREATE TRIGGER "triggerHashRolXUsuario"
BEFORE INSERT OR UPDATE ON "RolXUsuario"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashRolXUsuario"();

CREATE TRIGGER "triggerHashRolXPermiso"
BEFORE INSERT OR UPDATE ON "RolXPermiso"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashRolXPermiso"();

CREATE TRIGGER "triggerHashRol"
BEFORE INSERT OR UPDATE ON "Rol"
FOR EACH ROW
EXECUTE FUNCTION "calcularHashRol"();	
