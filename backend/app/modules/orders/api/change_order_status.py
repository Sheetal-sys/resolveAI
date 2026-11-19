
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import (
    ChangeOrderStatusRequest,
    OrderResponse,
)
from app.modules.orders.services.change_order_status import (
    ChangeOrderStatusService,
)
from app.shared.base.enums import RoleName


router = APIRouter()


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def change_order_status_endpoint(
    request: ChangeOrderStatusRequest,
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
    service = ChangeOrderStatusService(repository=repository)

    return service.change_status(
        order_id=order_id,
        request=request,
        current_user=current_user,
    )
