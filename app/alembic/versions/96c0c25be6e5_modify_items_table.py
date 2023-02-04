"""modify items table

Revision ID: 96c0c25be6e5
Revises: 
Create Date: 2023-02-04 10:51:23.781741

"""
from alembic import op
import sqlalchemy as sa


def column_exists(table_name, column_name):
    bind = op.get_context().bind
    insp = sa.inspect(bind)
    columns = insp.get_columns(table_name)
    return any(c["name"] == column_name for c in columns)


# revision identifiers, used by Alembic.
revision = "96c0c25be6e5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    if not column_exists(table_name="items", column_name="description"):
        op.add_column("items", sa.Column("description", sa.String()))
    if not column_exists(table_name="items", column_name="order_"):
        op.add_column("items", sa.Column("order_", sa.Integer()))


def downgrade() -> None:
    if column_exists(table_name="items", column_name="description"):
        op.remove_column("items", sa.Column("description", sa.String()))
    if column_exists(table_name="items", column_name="order_"):
        op.remove_column("items", sa.Column("order_", sa.Integer()))
