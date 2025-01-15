-- Trigger para check permiso de crear un expediente
CREATE TRIGGER "checkPermisoCrearExpediente"
BEFORE INSERT ON "Expediente" -- Aca cambiar y que sea solo para cuando 
                              -- el insert de Movimiento tenga un tramiteId que corresponda a crear un expediente
EXECUTE FUNCTION "triggerCheckPermisoCrearExpediente"();