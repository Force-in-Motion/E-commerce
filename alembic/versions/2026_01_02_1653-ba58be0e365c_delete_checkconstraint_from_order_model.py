"""delete CheckConstraint from order model

Revision ID: ba58be0e365c
Revises: 19f8f61eb46b
Create Date: 2026-01-02 16:53:16.043264

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ba58be0e365c"
down_revision: Union[str, Sequence[str], None] = "19f8f61eb46b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем check constraint, который проверял длину promo_code
    op.drop_constraint("err_promo_code_length", "orders", type_="check")

    # Преобразуем тип колонки из VARCHAR в INTEGER
    op.alter_column(
        "orders",
        "promo_code",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="promo_code::integer",
    )

    # Удаляем уникальный constraint, если больше не нужен
    op.drop_constraint(op.f("orders_promo_code_key"), "orders", type_="unique")


def downgrade() -> None:
    # Восстанавливаем уникальный constraint
    op.create_unique_constraint(
        op.f("orders_promo_code_key"),
        "orders",
        ["promo_code"],
        postgresql_nulls_not_distinct=False,
    )

    # Преобразуем колонку обратно в VARCHAR
    op.alter_column(
        "orders",
        "promo_code",
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True,
    )

    # Восстанавливаем check constraint
    op.create_check_constraint(
        "err_promo_code_length",
        "orders",
        "char_length(promo_code) <= 10"
    )
