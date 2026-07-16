from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Time, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.shared.base.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.tenant.models import Tenant


class TenantSettings(Base, TimestampMixin):
    __tablename__ = "tenant_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    support_email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    support_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        default="UTC",
        server_default=text("'UTC'"),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        default="English",
        server_default=text("'English'"),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(20),
        default="USD",
        server_default=text("'USD'"),
        nullable=False,
    )

    business_start_time: Mapped[time] = mapped_column(
        Time,
        default=time(9, 0),
        server_default=text("'09:00:00'"),
        nullable=False,
    )

    business_end_time: Mapped[time] = mapped_column(
        Time,
        default=time(18, 0),
        server_default=text("'18:00:00'"),
        nullable=False,
    )

    logo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    ai_confidence_threshold: Mapped[int] = mapped_column(
        Integer,
        default=85,
        server_default=text("85"),
        nullable=False,
    )

    auto_reply: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
    )

    auto_escalation: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
    )

    tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        back_populates="settings",
    )