from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.modules.orders.schemas.order_item_response import OrderItemResponse
from app.shared.base.enums import OrderStatus


class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_id: int
    status: OrderStatus
    currency: str
    subtotal: Decimal
    tax_amount: Decimal
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    ordered_at: datetime
    created_at: datetime
    updated_at: datetime | None
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
