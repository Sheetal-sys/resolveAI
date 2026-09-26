from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
