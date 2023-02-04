"""modify items table

Revision ID: 96c0c25be6e5
Revises: 
Create Date: 2023-02-04 10:51:23.781741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "96c0c25be6e5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_columns(
        "items",
        sa.Column("description", sa.String()),
        sa.Column("order_", sa.Integer()),
    )


def downgrade() -> None:
    pass
