from decimal import Decimal

from pydantic import BaseModel, Field


class OrderItemRequest(BaseModel):
    product_id: int = Field(..., gt=0)

    quantity: int = Field(
        ...,
        gt=0,
        description="Must be greater than zero",
    )

    unit_price: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Price per unit at time of order",
    )
