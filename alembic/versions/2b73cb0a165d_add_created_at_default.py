"""add created_at default"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2b73cb0a165d"
down_revision: Union[str, Sequence[str], None] = "2c66987205e2"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.alter_column(
        "articles",
        "created_at",
        server_default=sa.text("now()")
    )


def downgrade() -> None:

    op.alter_column(
        "articles",
        "created_at",
        server_default=None
    )