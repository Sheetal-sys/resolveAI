from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.services import RemoveCustomerService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_200_OK,
)
def remove_customer(
    customer_id: int,
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
    service = RemoveCustomerService(repository)

    return service.remove_customer(
        customer_id=customer_id,
        current_user=current_user,
    )