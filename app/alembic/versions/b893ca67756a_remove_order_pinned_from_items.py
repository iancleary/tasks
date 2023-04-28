"""remove_order_pinned_from_items

Revision ID: b893ca67756a
Revises: 96c0c25be6e5
Create Date: 2023-02-10 11:44:15.492209

"""
import sqlalchemy as sa

from alembic import op


def column_exists(table_name, column_name):
    bind = op.get_context().bind
    insp = sa.inspect(bind)
    columns = insp.get_columns(table_name)
    return any(c["name"] == column_name for c in columns)


# revision identifiers, used by Alembic.
revision = "b893ca67756a"
down_revision = "96c0c25be6e5"
branch_labels = None
depends_on = None

## op.drop_column note
### do not used named parameters
### It throws an operational error


def upgrade() -> None:
    if column_exists(table_name="items", column_name="order_"):
        op.drop_column("items", "order_")
    if column_exists(table_name="items", column_name="pinned"):
        op.drop_column("items", "pinned")


def downgrade() -> None:
    if not column_exists(table_name="items", column_name="order_"):
        op.add_column("items", sa.Column("order_", sa.Integer()))
    if not column_exists(table_name="items", column_name="pinned"):
        op.add_column("items", sa.Column("pinned", sa.Integer()))
