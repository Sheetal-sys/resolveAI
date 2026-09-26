from decimal import Decimal

from pydantic import BaseModel, Field


class OrderUpdateRequest(BaseModel):
    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    tax_amount: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    shipping_amount: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    discount_amount: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )
