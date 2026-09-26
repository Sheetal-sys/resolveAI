from decimal import Decimal

from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderResponse, OrderUpdateRequest
from app.shared.base.enums import OrderStatus


# Orders that have been shipped or completed cannot be financially edited
_LOCKED_STATUSES = {
    OrderStatus.SHIPPED.value,
    OrderStatus.DELIVERED.value,
    OrderStatus.CANCELLED.value,
}


class UpdateOrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def update_order(
        self,
        order_id: int,
        request: OrderUpdateRequest,
        current_user: CurrentUserResponse,
    ) -> OrderResponse:
        order = self.repository.get_by_id_and_tenant(
            order_id=order_id,
            tenant_id=current_user.tenant_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        if order.status in _LOCKED_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Order cannot be updated in status '{order.status}'"
                ),
            )

        update_data = request.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields were provided for update",
            )

        if "currency" in update_data:
            order.currency = update_data["currency"].upper().strip()

        if "tax_amount" in update_data:
            order.tax_amount = update_data["tax_amount"]

        if "shipping_amount" in update_data:
            order.shipping_amount = update_data["shipping_amount"]

        if "discount_amount" in update_data:
            order.discount_amount = update_data["discount_amount"]

        # Recalculate total after adjustments
        order.total_amount = (
            order.subtotal
            + order.tax_amount
            + order.shipping_amount
            - order.discount_amount
        ).quantize(Decimal("0.01"))

        try:
            self.repository.update(order)
            self.repository.commit()
            self.repository.refresh(order)

            return OrderResponse.model_validate(order)

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Order update failed: {str(exc)}",
            ) from exc
