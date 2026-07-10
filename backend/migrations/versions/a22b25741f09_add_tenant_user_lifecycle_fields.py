"""add tenant user lifecycle fields

Revision ID: a22b25741f09
Revises: 4b7a225d8daa
Create Date: 2026-07-10

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a22b25741f09"
down_revision: Union[str, Sequence[str], None] = "4b7a225d8daa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tenant_users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.add_column(
        "tenant_users",
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.add_column(
        "tenant_users",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_tenant_users_tenant_id"),
        "tenant_users",
        ["tenant_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_tenant_users_user_id"),
        "tenant_users",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_tenant_users_role_id"),
        "tenant_users",
        ["role_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_tenant_users_role_id"),
        table_name="tenant_users",
    )

    op.drop_index(
        op.f("ix_tenant_users_user_id"),
        table_name="tenant_users",
    )

    op.drop_index(
        op.f("ix_tenant_users_tenant_id"),
        table_name="tenant_users",
    )

    op.drop_column("tenant_users", "updated_at")
    op.drop_column("tenant_users", "joined_at")
    op.drop_column("tenant_users", "is_active")