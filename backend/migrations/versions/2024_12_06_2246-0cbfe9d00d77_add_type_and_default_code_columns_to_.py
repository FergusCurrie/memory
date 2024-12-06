"""add type and default_code columns to code table

Revision ID: 0cbfe9d00d77
Revises:
Create Date: 2024-12-06 22:46:25.722366

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "0cbfe9d00d77"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new column
    op.add_column("code", sa.Column("type", sa.String))
    op.execute("UPDATE code SET type = 'polars' WHERE type IS NULL")
    op.add_column("code", sa.Column("default_code", sa.String))
    op.execute("UPDATE code SET default_code = 'result = ()' WHERE default_code IS NULL")


def downgrade() -> None:
    op.drop_column("code", "type")
    op.drop_column("code", "default_code")
