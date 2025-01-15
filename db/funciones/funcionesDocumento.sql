/* PROCEDIMIENTOS ALMACENADOS PARA AUTOMATIZAR CARGAR LOS DATOS EN LA TABLA DOCUMENTO */

CREATE OR REPLACE FUNCTION public."crearDocumento"(
    p_cdd_id VARCHAR(50),
    p_nombre_archivo VARCHAR(255),
    p_tipo_documento VARCHAR(50),
    p_version_documento INT,
    p_cant_paginas INT,
    p_firmado BOOLEAN,
    p_activo BOOLEAN,
    p_hash_tabla VARCHAR(100)
) RETURNS TABLE(
    documento_id INT,
    firma_digital_id INT,
    cdd_id VARCHAR(50),
    nombre_archivo VARCHAR(255),
    tipo_documento VARCHAR(50),
    version_documento INT,
    cant_paginas INT,
    fecha_creacion TIMESTAMP,
    firmado BOOLEAN,
    estado BOOLEAN,
    documento_origen_id INT,
    qr_id VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE
    temp_documento_id INT;
    temp_fecha_creacion TIMESTAMP;
    temp_estado_documento BOOLEAN;
    temp_firmado_documento BOOLEAN;
    temp_hash_tabla VARCHAR(100);
BEGIN
    -- Verificar si ya existe un documento con el mismo cddId
    IF EXISTS(
        SELECT 1
        FROM "Documento"
        WHERE "cddId" = p_cdd_id
    ) THEN
        RAISE EXCEPTION 'Ya existe un documento esta referencia a cdd %', p_cdd_id;
    ELSE
        -- Si no existe, insertar el nuevo documento y devolver la fila insertada
        INSERT INTO "Documento"(
            "cddId", "nombreArchivo", "tipoDocumento", "versionDocumento", "cantPaginas", "firmado", "activo", "hashTabla"
        ) VALUES (
            p_cdd_id, p_nombre_archivo, p_tipo_documento, p_version_documento, p_cant_paginas, p_firmado, p_activo, 'HASHDUMP'
        )
        RETURNING "documentoId", "fechaCreacion", "Documento"."firmado" INTO temp_documento_id,temp_fecha_creacion, temp_firmado_documento;
        --Agregar Hash
        temp_hash_tabla := "calcularHashDocumento"(temp_documento_id);
        UPDATE "Documento"
        SET "hashTabla" = temp_hash_tabla
        WHERE "documentoId" = temp_documento_id;

        -- Devolver la fila completa
        RETURN QUERY SELECT
            temp_documento_id AS documento_id,
            CAST(NULL AS INT) AS firma_digital_id,
            p_cdd_id AS cdd_id,
            p_nombre_archivo AS nombre_archivo,
            p_tipo_documento AS tipo_documento,
            p_version_documento AS version_documento,
            p_cant_paginas AS cant_paginas,
            temp_fecha_creacion AS fecha_creacion,
            temp_firmado_documento AS firmado,
            CAST(NULL AS BOOLEAN) AS estado,
            CAST(NULL AS INT) AS documento_origen_id,
            CAST(NULL AS VARCHAR(100)) AS qr_id,
            p_activo AS activo,
            temp_hash_tabla AS hash_tabla;
    END IF;
END;
$$;


-- Función para obtener todos los documentos de un expediente
CREATE OR REPLACE FUNCTION public."obtenerDocumentosPorExpedienteId"(
    p_expediente_id INT
) RETURNS TABLE(
    documento_id INT,
    firma_digital_id INT,
    cdd_id VARCHAR(50),
    nombre_archivo VARCHAR(255),
    tipo_documento VARCHAR(50),
    version_documento INT,
    cant_paginas INT,
    fecha_creacion TIMESTAMP,
    firmado BOOLEAN,
    estado BOOLEAN,
    documento_origen_id INT,
    qr_id VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100),
    area_origen_id INT,
    area_destino_id INT,
    folios_inicial INT,
    folios_final INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_activo BOOLEAN;
BEGIN
    -- Verificar que el expediente exista y este activo
    SELECT "Expediente"."activo"
    INTO v_activo
    FROM "Expediente"
    WHERE "expedienteId" = p_expediente_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El expediente con id % no existe', p_expediente_id;
    END IF;
    IF NOT v_activo THEN
        RAISE EXCEPTION 'El expediente con id % no se encuentra activo', p_expediente_id;
    END IF;

    -- Devolver todos los documentos del expediente
    RETURN QUERY
    SELECT
        d."documentoId",
        d."firmaDigitalId",
        d."cddId",
        d."nombreArchivo",
        d."tipoDocumento",
        d."versionDocumento",
        d."cantPaginas",
        d."fechaCreacion",
        d."firmado",
        d."estado",
        d."documentoOrigenId",
        d."qrId",
        d."activo",
        d."hashTabla",

        m."areaOrigenId",
        m."areaDestinoId",
        dxm."foliosInicial",
        dxm."foliosFinal"
    FROM 
        "Movimiento" m
    JOIN 
        "DocumentoXMovimiento" dxm ON m."movimientoId" = dxm."movimientoId"
    JOIN
        "Documento" d ON dxm."documentoId" = d."documentoId"
    WHERE
        m."expedienteId" = p_expediente_id
    ORDER BY
        d."fechaCreacion" ASC;
END;
$$;

-- Función para obtener un documento por su id
CREATE OR REPLACE FUNCTION public."obtenerDocumentoPorId"(
    p_documento_id INT
) RETURNS TABLE(
    documento_id INT,
    firma_digital_id INT,
    cdd_id VARCHAR(50),
    nombre_archivo VARCHAR(255),
    tipo_documento VARCHAR(50),
    version_documento INT,
    cant_paginas INT,
    fecha_creacion TIMESTAMP,
    firmado BOOLEAN,
    estado BOOLEAN,
    documento_origen_id INT,
    qr_id VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100),
    area_origen_id INT,
    area_destino_id INT,
    folios_inicial INT,
    folios_final INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_activo BOOLEAN;
BEGIN
    -- Verificar que el documento exista y este activo
    SELECT "Documento"."activo"
    INTO v_activo
    FROM "Documento"
    WHERE "documentoId" = p_documento_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El documento con id % no existe', p_documento_id;
    END IF;

    -- Devolver el documento
    RETURN QUERY
    SELECT
        d."documentoId",
        d."firmaDigitalId",
        d."cddId",
        d."nombreArchivo",
        d."tipoDocumento",
        d."versionDocumento",
        d."cantPaginas",
        d."fechaCreacion",
        d."firmado",
        d."estado",
        d."documentoOrigenId",
        d."qrId",
        d."activo",
        d."hashTabla",

        m."areaOrigenId",
        m."areaDestinoId",

        dxm."foliosInicial",
        dxm."foliosFinal"
    FROM 
        "Movimiento" m
    JOIN
        "DocumentoXMovimiento" dxm ON m."movimientoId" = dxm."movimientoId"
    JOIN
        "Documento" d ON dxm."documentoId" = d."documentoId"
    WHERE
        d."documentoId" = p_documento_id;

END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerNombreYCddIdDocumentosPorExpedienteId"(
    p_expediente_id INT
) RETURNS TABLE(
    nombre_archivo VARCHAR(255),
    cdd_id VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_activo BOOLEAN;
BEGIN
    -- Verificar que el expediente exista y este activo
    SELECT "Expediente"."activo"
    INTO v_activo
    FROM "Expediente"
    WHERE "expedienteId" = p_expediente_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El expediente con id % no existe', p_expediente_id;
    END IF;

    -- Devolver solo los campos nombreArchivo y cddId del documento
    RETURN QUERY
    SELECT
        d."nombreArchivo",
        d."cddId"
    FROM 
        "Movimiento" m
    JOIN 
        "DocumentoXMovimiento" dxm ON m."movimientoId" = dxm."movimientoId"
    JOIN
        "Documento" d ON dxm."documentoId" = d."documentoId"
    WHERE
        m."expedienteId" = p_expediente_id
    ORDER BY
        d."fechaCreacion" ASC;
END;
$$;

CREATE OR REPLACE FUNCTION public."obtenerDocumentos"()
RETURNS TABLE(
    documento_id INT,
    firma_digital_id INT,
    cdd_id VARCHAR(50),
    nombre_archivo VARCHAR(255),
    tipo_documento VARCHAR(50),
    version_documento INT,
    cant_paginas INT,
    fecha_creacion TIMESTAMP,
    firmado BOOLEAN,
    estado BOOLEAN,
    documento_origen_id INT,
    qr_id VARCHAR(100),
    activo BOOLEAN,
    hash_tabla VARCHAR(100),
    area_origen_id INT,
    area_destino_id INT,
    folios_inicial INT,
    folios_final INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Devolver todos los documentos
    RETURN QUERY
    SELECT
        d."documentoId",
        d."firmaDigitalId",
        d."cddId",
        d."nombreArchivo",
        d."tipoDocumento",
        d."versionDocumento",
        d."cantPaginas",
        d."fechaCreacion",
        d."firmado",
        d."estado",
        d."documentoOrigenId",
        d."qrId",
        d."activo",
        d."hashTabla",

        m."areaOrigenId",
        m."areaDestinoId",
        dxm."foliosInicial",
        dxm."foliosFinal"
    FROM 
        "Movimiento" m
    JOIN 
        "DocumentoXMovimiento" dxm ON m."movimientoId" = dxm."movimientoId"
    JOIN
        "Documento" d ON dxm."documentoId" = d."documentoId"
    ORDER BY
        d."fechaCreacion" ASC;
END;
$$;
   