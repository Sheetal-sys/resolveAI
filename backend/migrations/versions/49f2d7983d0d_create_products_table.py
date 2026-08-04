"""create products table

Revision ID: 49f2d7983d0d
Revises: ba8b1e8c06cc
Create Date: 2026-08-04 14:51:26.445896
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "49f2d7983d0d"
down_revision: Union[str, Sequence[str], None] = "ba8b1e8c06cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "product_code",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "sku",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "brand",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "price",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=10),
            nullable=False,
            server_default=sa.text("'USD'"),
        ),
        sa.Column(
            "stock_quantity",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'ACTIVE'"),
        ),
        sa.Column(
            "image_url",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "sku",
            name="uq_product_tenant_sku",
        ),
    )

    op.create_index(
        op.f("ix_products_id"),
        "products",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_products_tenant_id"),
        "products",
        ["tenant_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_products_tenant_id"),
        table_name="products",
    )

    op.drop_index(
        op.f("ix_products_id"),
        table_name="products",
    )

    op.drop_table("products")