from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import (
    CustomerResponse,
    CustomerUpdateRequest,
)
from app.modules.customer.services import UpdateCustomerService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    request: CustomerUpdateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles(
            [
                RoleName.TENANT_ADMIN.value,
                RoleName.SUPERVISOR.value,
                RoleName.SUPPORT_AGENT.value,
            ]
        )
    ),
):
    repository = CustomerRepository(db)
    service = UpdateCustomerService(repository)

    return service.update_customer(
        customer_id=customer_id,
        request=request,
        current_user=current_user,
    )