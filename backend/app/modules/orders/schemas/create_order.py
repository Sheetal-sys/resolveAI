from decimal import Decimal

from pydantic import BaseModel, Field

from app.modules.orders.schemas.order_item_request import OrderItemRequest


class OrderCreateRequest(BaseModel):
    customer_id: int = Field(..., gt=0)

    currency: str = Field(
        default="USD",
        min_length=3,
        max_length=3,
    )

    tax_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        decimal_places=2,
    )

    shipping_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        decimal_places=2,
    )

    discount_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        decimal_places=2,
    )

    items: list[OrderItemRequest] = Field(
        ...,
        min_length=1,
        description="At least one order item is required",
    )
