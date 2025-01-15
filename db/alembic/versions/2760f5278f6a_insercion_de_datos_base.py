"""Insercion de datos base

Revision ID: 2760f5278f6a
Revises: 08eaf4d947c7
Create Date: 2024-10-25 09:00:03.460097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2760f5278f6a'
down_revision: Union[str, None] = '6bc1a8df2378'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Agregar expediente tipo expediente
    op.execute(
        """
        INSERT INTO "TipoExpediente" ("nombreTipoExpediente", "descripcionTipoExpediente", "hashTabla", "activo")
            VALUES 
                ('Expediente', 'Expediente tipo expediente', 'AGREGAR HASH', true);
        """
    )
    # Actualizar la columna hashTabla de TipoExpediente
    op.execute(
        """
        UPDATE "TipoExpediente"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("tipoExpedienteId"::TEXT, '') ||
            COALESCE("nombreTipoExpediente"::TEXT, '') ||
            COALESCE("descripcionTipoExpediente"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )

   # Agregar permisos Crear, Consultar, Mover
    op.execute(
        """
        INSERT INTO "Permiso" ("nombrePermiso", "descripcionPermiso", "hashTabla", "activo")
            VALUES
                ('Crear Expediente', 'Crear expediente', 'AGREGAR HASH1', true),
                ('Consultar Expediente', 'Consultar expediente', 'AGREGAR HASH2', true),
                ('Mover Expediente', 'Mover expediente', 'AGREGAR HASH3', true),
                ('Recibir Expediente', 'Recibir expediente', 'AGREGAR HASH4', true),
                ('Protocolizar Expediente', 'Protocolizar expediente', 'AGREGAR HASH5', true),
                ('Archivar Expediente', 'Archivar expediente', 'AGREGAR HASH6', true),
                
                ('Crear Rol', 'Crear rol', 'AGREGAR HASH7', true),
                ('Eliminar Rol', 'Eliminar rol', 'AGREGAR HASH8', true),
                ('Crear Permiso', 'Crear un nuevo permiso', 'AGREGAR HASH9', true),
                ('Eliminar Permiso', 'Eliminar un permiso', 'AGREGAR HASH10', true),
                ('Crear Administrador', 'Crear un nuevo administrador', 'AGREGAR HASH11', true),
                ('Eliminar Administrador', 'Eliminar un administrador', 'AGREGAR HASH12', true),
                ('Validar baja Sistema Vertical', 'Validar baja de un sistema vertical', 'AGREGAR HASH13', true),
                ('Auditar', 'Permite visualizar informacion de auditoria', 'AGREGAR HASH14', true),

                ('Dar de alta Sistema Vertical', 'Dar de alta un sistema vertical', 'AGREGAR HASH15', true),
                ('Dar de baja Sistema Vertical', 'Dar de baja un sistema vertical', 'AGREGAR HASH16', true),

                ('Crear Super Admin', 'Crear un nuevo super admin', 'AGREGAR HASH17', true),
               
                ('Pedido dar de baja Sistema Vertical', 'Pedido dar de baja un sistema vertical', 'AGREGAR HASH18', true),

                ('Crear rol con permiso', 'Asociar un permiso existente a un rol existente', 'AGREGAR HASH19', true),

                ('Cambiar rol Usuario', 'Al revocar el rol a un usuario, este pasara a ser Usuario Fisico', 'AGREGAR HASH20', true);
            

        """
    )
    # Actualizar la columna hashTabla de Permiso
    op.execute(
        """
        UPDATE "Permiso"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("permisoId"::TEXT, '') ||
            COALESCE("nombrePermiso"::TEXT, '') ||
            COALESCE("descripcionPermiso"::TEXT, '') ||
            COALESCE("fechaCreacion"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )
    # Agregar roles
    op.execute(
        """
        INSERT INTO "Rol" ("nombreRol", "descripcionRol", "hashTabla", "activo")
            VALUES
                ('Super Admin', 'Usuario creador de roles, permisos y asigna el rol de administrador', 'AGREGAR HASH1', true),
                ('Administrador', 'Usuario que puede designar permisos a otros usuarios', 'AGREGAR HASH2', true),
                ('Usuario Aplicacion', 'Usuario perteneciente a un sistema vertical', 'AGREGAR HASH3', true),
                ('Usuario Fisico', 'Usuario físico entrando por VEDI.', 'AGREGAR HASH4', true);
        """
    )
    # Actualizar la columna hashTabla de Rol
    op.execute(
        """
        UPDATE "Rol"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("rolId"::TEXT, '') ||
            COALESCE("nombreRol"::TEXT, '') ||
            COALESCE("descripcionRol"::TEXT, '') ||
            COALESCE("fechaCreacion"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%'; 
        """
    )
    # Agregar relacion entre rol y permisos
    op.execute(
        """
        INSERT INTO "RolXPermiso" ("rolId", "permisoId", "hashTabla", "activo")
            VALUES
                (1, 2, 'AGREGAR HASH1', true),
                (1, 7, 'AGREGAR HASH2', true),
                (1, 8, 'AGREGAR HASH3', true),
                (1, 9, 'AGREGAR HASH4', true),
                (1, 10, 'AGREGAR HASH5', true),
                (1, 11, 'AGREGAR HASH6', true),
                (1, 12, 'AGREGAR HASH7', true),
                (1, 13, 'AGREGAR HASH8', true),
                (1, 14, 'AGREGAR HASH9', true),
                (1, 16, 'AGREGAR HASH10', true),
                (1, 17, 'AGREGAR HASH11', true),
                (1, 19, 'AGREGAR HASH12', true),
                (1, 20, 'AGREGAR HASH13', true),

                (2, 15, 'AGREGAR HASH14', true),
                (2, 18, 'AGREGAR HASH15', true),
                (2, 20, 'AGREGAR HASH16', true),

                (3, 1, 'AGREGAR HASH17', true),
                (3, 2, 'AGREGAR HASH18', true),
                (3, 3, 'AGREGAR HASH19', true),
                (3, 4, 'AGREGAR HASH20', true),
                (3, 5, 'AGREGAR HASH21', true),
                (3, 6, 'AGREGAR HASH22', true),
 
                (4, 2, 'AGREGAR HASH23', true);
        """
    )
    # Actualizar la columna hashTabla de RolXPermiso
    op.execute(
        """
        UPDATE "RolXPermiso"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("rolXPermisoId"::TEXT, '') ||
            COALESCE("permisoId"::TEXT, '') ||
            COALESCE("rolId"::TEXT, '') ||
            COALESCE("fechaCreacion"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )
    # Agregar usuario
    op.execute(
        """
        INSERT INTO "Usuario" ("cuilUsuario", "nombreUsuario", "areaId", "aplicacionVediId", "apiKey", "usuarioAlta","hashTabla", "activo")
            VALUES
                ('20111111116', 'SuperAdmin', 5280, 0, 'asdf', 0, 'AGREGAR HASH1', true),
                ('20123453456', 'Admin', 5280, 1, 'qwer', 1, 'AGREGAR HASH2', true),
                (NULL, 'usuarioAplicacion', 5280, 3, 'zxcv', 2, 'AGREGAR HASH3', true),
                ('20364306629', 'Hilario', 5280, 4, '1234', 3, 'AGREGAR HASH4', true);
        """
    )
    # Actualizar la columna hashTabla de Usuario
    op.execute(
        """
        UPDATE "Usuario"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("usuarioId"::TEXT, '') ||
            COALESCE("cuilUsuario"::TEXT, '') ||
            COALESCE("nombreUsuario"::TEXT, '') ||
            COALESCE("fechaCreacion"::TEXT, '') ||
            COALESCE("fechaBaja"::TEXT, '') ||
            COALESCE("areaId"::TEXT, '') ||
            COALESCE("aplicacionVediId"::TEXT, '') ||
            COALESCE("apiKey"::TEXT, '') ||
            COALESCE("usuarioAlta"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )
    # Agregar relacion entre usuario y rol
    op.execute(
        """
        INSERT INTO "RolXUsuario" ("usuarioId", "rolId", "hashTabla", "activo")
            VALUES
                (1, 1, 'AGREGAR HASH1', true),
                (2, 2, 'AGREGAR HASH2', true),
                (3, 3, 'AGREGAR HASH3', true),
                (4, 1, 'AGREGAR HASH4', true),
                (4, 2, 'AGREGAR HASH5', true),
                (4, 3, 'AGREGAR HASH6', true);
        """
    )
    # Actualizar la columna hashTabla de RolXUsuario
    op.execute(
        """
        UPDATE "RolXUsuario"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("rolXUsuarioId"::TEXT, '') ||
            COALESCE("usuarioId"::TEXT, '') ||
            COALESCE("rolId"::TEXT, '') ||
            COALESCE("fechaCreacion"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )

    # Agregar un tipo de norma
    op.execute(
        """
        INSERT INTO "TipoNorma" ("nombreTipoNorma", "descripcionTipoNorma", "hashTabla", "activo")
            VALUES
                ('Norma Default', 'Norma', 'AGREGAR HASH', true);
        """
    )
    # Actualizar la columna hashTabla de TipoNorma
    op.execute(
        """
        UPDATE "TipoNorma"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("tipoNormaId"::TEXT, '') ||
            COALESCE("nombreTipoNorma"::TEXT, '') ||
            COALESCE("descripcionTipoNorma"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )

    # Agregar algunos estados de expedientes
    op.execute(
        """
        INSERT INTO "EstadoExpediente" ("nombreEstadoExpediente", "descripcionEstadoExpediente", "hashTabla", "activo")
            VALUES
                ('En proceso', 'Expediente en proceso','AGREGAR HASH10', true),
                ('En revision', 'Expediente en revision','AGREGAR HASH2', true),
                ('En espera', 'Expediente en espera','AGREGAR HASH3', true),
                ('Creado', 'Expediente creado','AGREGAR HASH4', true);
        """
    )

    # Actualizar la columna hashTabla de TipoExpediente
    op.execute(
        """
        UPDATE "EstadoExpediente"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("estadoExpedienteId"::TEXT, '') ||
            COALESCE("nombreEstadoExpediente"::TEXT, '') ||
            COALESCE("descripcionEstadoExpediente"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )

    # Insercion tipo notificacion 'baja'
    op.execute(
        """
        INSERT INTO "TipoNotificacion" ("nombreTipoNotificacion", "descripcionTipoNotificacion", "hashTabla", "activo")
            VALUES
                ('Baja', 'Notificacion de baja', 'AGREGAR HASH', true);
        """
    )
    # Actualizar la columna hashTabla de TipoNotificacion
    op.execute(
        """
        UPDATE "TipoNotificacion"
        SET "hashTabla" = "calcularHashSha256"(
            COALESCE("tipoNotificacionId"::TEXT, '') ||
            COALESCE("nombreTipoNotificacion"::TEXT, '') ||
            COALESCE("descripcionTipoNotificacion"::TEXT, '') ||
            COALESCE("activo"::TEXT, '')
        )
        WHERE "hashTabla" LIKE 'AGREGAR HASH%';
        """
    )

    # op.execute(
    # En caso de ser necesario, habria que modificar usarioCreadorId por los cambios que introdujimos a expediente manejando los dos ID distintos de creador fisico y aplicacion
    #     """
    #     INSERT INTO "Expediente" ("tipoExpedienteId","expedientePadreId","numeroExpediente","areaIniciadoraId",
    #         "usuarioCreadorId","asuntoExpediente","fechaUltimoMovimiento","visibilidadExpediente","activo",
    #         "hashTabla","foliosApertura","temaNombre","areaActualidadId","foliosActuales","documentoSiradId"
    #     ) VALUES (
    #         1,0,'EXP-12345',2,3,'Asunto de prueba para el expediente',NOW(),'Público',TRUE,
    #         'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',10,'Tema de prueba para SIRAD',
    #         1,0,NULL  -- documentoSiradId (puede ser NULL si no aplica)
    #     );
    #     """
    # )

    # op.execute(
    #     """ INSERT INTO "HistorialEstadoExpediente" ("expedienteId","estadoExpedienteId","fechaDesde","fechaHasta","hashTabla","activo")	
    # 	    VALUES (1, 4, NOW(), NULL, 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890', TRUE);
    #     """
    # )
    
    # ### end Alembic commands ###


def downgrade() -> None:
    # Eliminar RolXPermiso
    op.execute(
        """
        DELETE FROM "RolXPermiso";
        """
    )
    # Eliminar RolXUsuario
    op.execute(
        """
        DELETE FROM "RolXUsuario";
        """
    )
    # Eliminar Rol
    op.execute(
        """
        DELETE FROM "Rol";
        """
    )
    # Eliminar permisos Crear, Consultar, Mover
    op.execute(
        """
        DELETE FROM "Permiso";
        """
    )
    # Eliminar historial de estados de expediente
    op.execute(
        """
        DELETE FROM "HistorialEstadoExpediente";
        """
    )
    # Eliminar documentoxmovimiento
    op.execute(
        """
        DELETE FROM "DocumentoXMovimiento";
        """
    )
    # Delete records from Movimiento
    op.execute(
        """
        DELETE FROM "Movimiento";
        """
    )
    # Delete records from Expediente
    op.execute(
        """
        DELETE FROM "Expediente";
        """
    )
    # Eliminar expediente tipo expediente
    op.execute(
        """
        DELETE FROM "TipoExpediente";
        """
    )
    # Elminiar una norma
    op.execute(
        """
        DELETE FROM "Norma";	
        """	
    )
    # Eliminar un tipo de norma
    op.execute(
        """
        DELETE FROM "TipoNorma";
        """
    )
    # Eliminar notificaciones
    op.execute(
        """
        DELETE FROM "Notificacion";
        """
    )
     # Eliminar un tipo de notificacion
    op.execute(
        """
        DELETE FROM "TipoNotificacion";
        """
    )
    # Eliminar algunos estados de expedientes
    op.execute(
        """
        DELETE FROM "EstadoExpediente";
        """
    )
    # Eliminar Usuario
    op.execute(
        """
        DELETE FROM "Usuario";
        """
    )
