from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import (
    ChangeCustomerStatusRequest,
    CustomerResponse,
)
from app.modules.customer.services import ChangeCustomerStatusService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.patch(
    "/{customer_id}/status",
    response_model=CustomerResponse,
)
def change_customer_status(
    customer_id: int,
    request: ChangeCustomerStatusRequest,
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
    repository = CustomerRepository(db)
    service = ChangeCustomerStatusService(repository)

    return service.change_status(
        customer_id=customer_id,
        request=request,
        current_user=current_user,
    )