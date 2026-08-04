from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import (
    CustomerCreateRequest,
    CustomerResponse,
)
from app.modules.customer.services import CreateCustomerService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    request: CustomerCreateRequest,
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
    service = CreateCustomerService(repository)

    return service.create_customer(
        request=request,
        current_user=current_user,
    )