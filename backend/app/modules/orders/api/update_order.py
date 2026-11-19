
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderResponse, OrderUpdateRequest
from app.modules.orders.services.update_order import UpdateOrderService
from app.shared.base.enums import RoleName


router = APIRouter()


@router.patch(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def update_order_endpoint(
    request: OrderUpdateRequest,
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles(
            [
                RoleName.TENANT_ADMIN.value,
                RoleName.SUPERVISOR.value,
            ]
        )
    ),
):
    repository = OrderRepository(db)
    service = UpdateOrderService(repository=repository)

    return service.update_order(
        order_id=order_id,
        request=request,
        current_user=current_user,
    )
