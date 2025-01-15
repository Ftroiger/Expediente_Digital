"""Funciones Completar Auditoria

Revision ID: 3d4ec17600ed
Revises: 3f9496e0e01c
Create Date: 2024-11-27 08:53:27.330479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from db.databaseUtils import _read_sql_file

# revision identifiers, used by Alembic.
revision: str = '3d4ec17600ed'
down_revision: Union[str, None] = '3f9496e0e01c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql_functions = _read_sql_file('funciones/funcionesCompletarAuditoria.sql')
    op.execute(sql_functions)
   


def downgrade() -> None:
    sql_drop_functions = _read_sql_file('funciones/dropFuncionesCompletarAuditoria.sql')
    op.execute(sql_drop_functions)
    # ### end Alembic commands ###
