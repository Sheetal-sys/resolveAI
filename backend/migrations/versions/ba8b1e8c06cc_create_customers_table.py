"""create customers table

Revision ID: ba8b1e8c06cc
Revises: 0404551af949
Create Date: 2026-08-02 20:02:25.868339
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision: str = "ba8b1e8c06cc"
down_revision: Union[str, Sequence[str], None] = "0404551af949"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customers",
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
            "customer_code",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "first_name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "last_name",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "email",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "phone",
            sa.String(length=30),
            nullable=True,
        ),
        sa.Column(
            "company",
            sa.String(length=150),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default=sa.text("'ACTIVE'"),
        ),
        sa.Column(
            "source",
            sa.String(length=30),
            nullable=False,
            server_default=sa.text("'WEBSITE'"),
        ),
        sa.Column(
            "internal_notes",
            sa.Text(),
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
            "customer_code",
            name="uq_customer_tenant_code",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "email",
            name="uq_customer_tenant_email",
        ),
    )

    op.create_index(
        op.f("ix_customers_id"),
        "customers",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_customers_tenant_id"),
        "customers",
        ["tenant_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_customers_tenant_id"),
        table_name="customers",
    )

    op.drop_index(
        op.f("ix_customers_id"),
        table_name="customers",
    )

    op.drop_table("customers")