from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.shared.base.enums import OrderStatus
from app.shared.base.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.customer.models import Customer
    from app.modules.products.models import Product
    from app.modules.tenant.models import Tenant


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "order_number",
            name="uq_order_tenant_number",
        ),
    )

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

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    order_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default=OrderStatus.PENDING.value,
        server_default=text("'PENDING'"),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD",
        server_default=text("'USD'"),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        server_default=text("0.00"),
        nullable=False,
    )

    shipping_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        server_default=text("0.00"),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        server_default=text("0.00"),
        nullable=False,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    ordered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        back_populates="orders",
    )

    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="orders",
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

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

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    # Relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="order_items",
    )
