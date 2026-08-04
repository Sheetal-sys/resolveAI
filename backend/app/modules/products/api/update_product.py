from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.products.schemas import (
    ProductResponse,
    ProductUpdateRequest,
)
from app.modules.products.services import update_product
from app.shared.base.enums import RoleName

router = APIRouter()


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product_endpoint(
    product_id: int,
    request: ProductUpdateRequest,
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
    return update_product(
        db=db,
        tenant_id=current_user.tenant_id,
        product_id=product_id,
        request=request,
    )