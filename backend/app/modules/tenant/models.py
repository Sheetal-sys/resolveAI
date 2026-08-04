from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.shared.base.enums import SubscriptionPlan, TenantStatus
from app.shared.base.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.customer.models import Customer
    from app.modules.products.models import Product
    from app.modules.role.models import Role
    from app.modules.tenant_settings.models import TenantSettings
    from app.modules.user.models import User


class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    subscription_plan: Mapped[str] = mapped_column(
        String(50),
        default=SubscriptionPlan.STARTER.value,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default=TenantStatus.ACTIVE.value,
        nullable=False,
    )

    settings: Mapped["TenantSettings | None"] = relationship(
        "TenantSettings",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    customers: Mapped[list["Customer"]] = relationship(
        "Customer",
        back_populates="tenant",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="tenant",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class TenantUser(Base):
    __tablename__ = "tenant_users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )

    tenant: Mapped["Tenant"] = relationship(
        "Tenant",
    )

    user: Mapped["User"] = relationship(
        "User",
    )

    role: Mapped["Role"] = relationship(
        "Role",
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "user_id",
            name="uq_tenant_user",
        ),
    )