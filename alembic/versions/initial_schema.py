"""initial schema

Revision ID: initial
Revises:
Create Date: 2025-10-03 16:30:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = "initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- Users ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    )

    # --- Profiles ---
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("bio", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    )

    # --- Products ---
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("price", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    )

    # --- Orders ---
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("total_sum", sa.Integer, nullable=False, server_default="0"),
        sa.Column("comment", sa.String, nullable=True),
        sa.Column("promo_code", sa.String(10), unique=True, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.CheckConstraint(
            "promo_code IS NULL OR char_length(promo_code) = 10",
            name="err_promo_code_length",
        ),
    )

    # --- OrderProducts ---
    op.create_table(
        "order_products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "order_id",
            sa.Integer,
            sa.ForeignKey("orders.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.Integer,
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    # --- Carts ---
    op.create_table(
        "carts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    )

    # --- CartProducts ---
    op.create_table(
        "cart_products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "cart_id",
            sa.Integer,
            sa.ForeignKey("carts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.Integer,
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("cart_products")
    op.drop_table("carts")
    op.drop_table("order_products")
    op.drop_table("orders")
    op.drop_table("products")
    op.drop_table("profiles")
    op.drop_table("users")
