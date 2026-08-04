from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import CustomerResponse
from app.modules.customer.services import GetCustomerService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
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
    service = GetCustomerService(repository)

    return service.get_customer(
        customer_id=customer_id,
        current_user=current_user,
    )