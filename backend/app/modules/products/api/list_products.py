from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.products.schemas import ProductListResponse
from app.modules.products.services import list_products
from app.shared.base.enums import RoleName

router = APIRouter()


@router.get(
    "/",
    response_model=ProductListResponse,
)
def list_products_endpoint(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
    ),
    product_status: str | None = Query(
        default=None,
        pattern="^(ACTIVE|INACTIVE)$",
    ),
    category: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
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
    return list_products(
        db=db,
        tenant_id=current_user.tenant_id,
        skip=skip,
        limit=limit,
        search=search,
        product_status=product_status,
        category=category,
    )