from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import ChangeOrderStatusRequest, OrderResponse
from app.shared.base.enums import OrderStatus


# Define valid forward transitions only
_VALID_TRANSITIONS: dict[str, set[str]] = {
    OrderStatus.PENDING.value: {
        OrderStatus.CONFIRMED.value,
        OrderStatus.CANCELLED.value,
    },
    OrderStatus.CONFIRMED.value: {
        OrderStatus.PROCESSING.value,
        OrderStatus.CANCELLED.value,
    },
    OrderStatus.PROCESSING.value: {
        OrderStatus.SHIPPED.value,
        OrderStatus.CANCELLED.value,
    },
    OrderStatus.SHIPPED.value: {
        OrderStatus.DELIVERED.value,
    },
    OrderStatus.DELIVERED.value: set(),
    OrderStatus.CANCELLED.value: set(),
}


class ChangeOrderStatusService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def change_status(
        self,
        order_id: int,
        request: ChangeOrderStatusRequest,
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

        new_status = request.status.value
        current_status = order.status

        if new_status == current_status:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Order is already in status '{current_status}'",
            )

        allowed_next = _VALID_TRANSITIONS.get(current_status, set())

        if new_status not in allowed_next:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Cannot transition order from '{current_status}' "
                    f"to '{new_status}'"
                ),
            )

        try:
            order.status = new_status
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
                detail=f"Order status change failed: {str(exc)}",
            ) from exc
