"""add field role for user model

Revision ID: b15fabb336c2
Revises: b91d3f6639e8
Create Date: 2025-12-05 14:36:48.328791
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b15fabb336c2"
down_revision: Union[str, Sequence[str], None] = "b91d3f6639e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ENUM нужно держать ссылкой, чтобы использовать и в upgrade, и в downgrade
userrole_enum = sa.Enum(
    "god", "user", "admin", "moderator",
    name="userrole"
)

def upgrade() -> None:
    # 1. Создать ENUM тип
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # 2. Добавить колонку, использующую этот ENUM
    op.add_column(
        "users",
        sa.Column("role", userrole_enum, nullable=False, server_default="user")
    )

    # Удаляем server_default теперь, когда колонка создана
    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    # 1. Удалить колонку
    op.drop_column("users", "role")

    # 2. Удалить ENUM тип
    userrole_enum.drop(op.get_bind(), checkfirst=True)
