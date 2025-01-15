from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from db.database import Base
from db.models.documento import Documento
from db.models.documentoXMovimiento import DocumentoXMovimiento
from db.models.estadoExpediente import EstadoExpediente
from db.models.expediente import Expediente
from db.models.expedienteXNorma import ExpedienteXNorma
from db.models.historialEstadoExpediente import HistorialEstadoExpediente
from db.models.movimiento import Movimiento
from db.models.norma import Norma
from db.models.permiso import Permiso
from db.models.tipoExpediente import TipoExpediente
from db.models.tipoNorma import TipoNorma
from db.models.auditoria import rolXUsuarioAud,rolAuditoria,rolXPermisoAud,usuarioAud,documentoAud, documentoXMovimientoAud, estadoExpedienteAud, expedienteAud, expedienteXNormaAud, historialEstadoExpedienteAud, movimientoAud, normaAud, permisoAud, tipoExpedienteAud, tipoNormaAud, notificacionAud, tipoNotificacionAud
from db.models.usuario import Usuario
from db.models.rol import Rol
from db.models.rolXPermiso import RolXPermiso
from db.models.rolXUsuario import RolXUsuario
from db.models.notificacion import Notificacion
from db.models.tipoNotificacion import TipoNotificacion
import os
from dotenv import load_dotenv

load_dotenv()

database_url=os.getenv("URL_BASE_DE_DATOS")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

if database_url:
    config.set_main_option("sqlalchemy.url",database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
