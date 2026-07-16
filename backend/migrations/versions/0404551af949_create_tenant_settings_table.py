"""create tenant settings table

Revision ID: 0404551af949
Revises: a22b25741f09
Create Date: 2026-07-17 02:01:52.163170
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision: str = "0404551af949"
down_revision: Union[str, Sequence[str], None] = "a22b25741f09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tenant_settings",
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
            "website",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "support_email",
            sa.String(length=150),
            nullable=True,
        ),
        sa.Column(
            "support_phone",
            sa.String(length=30),
            nullable=True,
        ),
        sa.Column(
            "timezone",
            sa.String(length=100),
            nullable=False,
            server_default=sa.text("'UTC'"),
        ),
        sa.Column(
            "language",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'English'"),
        ),
        sa.Column(
            "currency",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'USD'"),
        ),
        sa.Column(
            "business_start_time",
            sa.Time(),
            nullable=False,
            server_default=sa.text("'09:00:00'"),
        ),
        sa.Column(
            "business_end_time",
            sa.Time(),
            nullable=False,
            server_default=sa.text("'18:00:00'"),
        ),
        sa.Column(
            "logo_url",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "ai_confidence_threshold",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("85"),
        ),
        sa.Column(
            "auto_reply",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "auto_escalation",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
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
    )

    op.create_index(
        op.f("ix_tenant_settings_id"),
        "tenant_settings",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_tenant_settings_tenant_id"),
        "tenant_settings",
        ["tenant_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_tenant_settings_tenant_id"),
        table_name="tenant_settings",
    )

    op.drop_index(
        op.f("ix_tenant_settings_id"),
        table_name="tenant_settings",
    )

    op.drop_table("tenant_settings")