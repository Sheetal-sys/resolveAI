from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.shared.base.enums import CustomerSource, CustomerStatus
from app.shared.base.models import TimestampMixin
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)

if TYPE_CHECKING:
    from app.modules.tenant.models import Tenant


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
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

    customer_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    company: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
    String(30),
    default=CustomerStatus.ACTIVE.value,
    server_default=text("'ACTIVE'"),
    nullable=False,
)

    source: Mapped[str] = mapped_column(
    String(30),
    default=CustomerSource.WEBSITE.value,
    server_default=text("'WEBSITE'"),
    nullable=False,
)

    internal_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        back_populates="customers",
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "customer_code",
            name="uq_customer_tenant_code",
        ),
        UniqueConstraint(
            "tenant_id",
            "email",
            name="uq_customer_tenant_email",
        ),
    )