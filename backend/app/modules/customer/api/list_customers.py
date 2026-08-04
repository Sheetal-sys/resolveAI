from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import CustomerListResponse
from app.modules.customer.services import ListCustomersService
from app.shared.base.enums import (
    CustomerSource,
    CustomerStatus,
    RoleName,
)

router = APIRouter()


@router.get(
    "/",
    response_model=CustomerListResponse,
)
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = None,
    customer_status: CustomerStatus | None = None,
    source: CustomerSource | None = None,
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
    service = ListCustomersService(repository)

    return service.list_customers(
        current_user=current_user,
        skip=skip,
        limit=limit,
        search=search,
        customer_status=customer_status,
        source=source,
    )