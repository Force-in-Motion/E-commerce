"""delete CheckConstraint from order model

Revision ID: 1b454fc638c7
Revises: ba58be0e365c
Create Date: 2026-01-02 17:03:04.446633

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1b454fc638c7"
down_revision: Union[str, Sequence[str], None] = "ba58be0e365c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем check constraint, если он существует
    with op.get_context().autocommit_block():
        op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'err_promo_code_length'
            ) THEN
                ALTER TABLE orders DROP CONSTRAINT err_promo_code_length;
            END IF;
        END$$;
        """)

    # Преобразуем тип колонки из VARCHAR в INTEGER
    op.alter_column(
        "orders",
        "promo_code",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="promo_code::integer",
    )

    # Удаляем уникальный constraint, если он существует
    with op.get_context().autocommit_block():
        op.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'orders_promo_code_key'
            ) THEN
                ALTER TABLE orders DROP CONSTRAINT orders_promo_code_key;
            END IF;
        END$$;
        """)


def downgrade() -> None:
    # Восстанавливаем уникальный constraint
    op.create_unique_constraint(
        "orders_promo_code_key",
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
