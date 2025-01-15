/* PROCEDIMIENTOS ALMACENADOS PARA AUTOMATIZAR CARGAR LOS DATOS EN LA TABLA DOCUMENTOXMOVIMIENTO */

/* Se modifico a una funcion que retorna una tabla con el id de la relacion y un mensaje por las 
   funciones que definimos en db utils. Ahora es necesario pasarle un parametro y que a su vez
   devuelva parametros para luego pasarlos al router */

CREATE OR REPLACE FUNCTION public."crearRelacion"(
    p_movimiento_id INT,
    p_documento_id INT,
    p_folios_inicial INT,
    p_folios_final INT,
    p_activo BOOLEAN
) RETURNS TABLE(
    documento_x_movimiento_id INT,
    movimiento_id INT,
    documento_id INT,
    folios_inicial INT,
    folios_final INT,
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE
    temp_documento_x_movimiento_id INT;
    temp_hash_tabla VARCHAR(100);
BEGIN
    -- Verificar si ya existe una relación con el mismo movimientoId y documentoId
    IF EXISTS (
        SELECT 1
        FROM "DocumentoXMovimiento"
        WHERE movimiento_id = p_movimiento_id
        AND documento_id = p_documento_id
    ) THEN
        -- Si ya existe, devolver la tupla encontrada
        RAISE EXCEPTION 'Ya existe una relación con este id de movimiento: % e id de documento: %', p_movimiento_id, p_documento_id;
    ELSE
        -- Si no existe, insertar la nueva relación y devolver la fila insertada
        INSERT INTO "DocumentoXMovimiento" (
            "movimientoId", "documentoId", "foliosInicial", "foliosFinal", "activo", "hashTabla"
        ) VALUES (
            p_movimiento_id, p_documento_id, p_folios_inicial, p_folios_final, p_activo, 'HASHDUMP'
        )
        RETURNING "documentoXMovimientoId" INTO temp_documento_x_movimiento_id;
        
        --Agregar Hash
        temp_hash_tabla := "calcularHashDocumentoXMovimiento"(temp_documento_x_movimiento_id);
        UPDATE "DocumentoXMovimiento"
        SET "hashTabla" = temp_hash_tabla
        WHERE "documentoXMovimientoId" = temp_documento_x_movimiento_id;
        -- Devolver la fila completa
        RETURN QUERY SELECT 
            temp_documento_x_movimiento_id AS documentoXMovimientoId,
            p_movimiento_id AS movimientoId, 
            p_documento_id AS documentoId, 
            p_folios_inicial AS foliosInicial, 
            p_folios_final AS foliosFinal, 
            p_activo AS activo, 
            temp_hash_tabla AS hashTabla;
    END IF;
END;
$$;
