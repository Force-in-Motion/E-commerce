"""create tables

Revision ID: a3bbe1fda0fe
Revises:
Create Date: 2025-07-06 20:29:28.885027

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "a3bbe1fda0fe"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
