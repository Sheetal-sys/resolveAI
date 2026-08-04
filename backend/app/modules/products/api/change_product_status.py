from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.products.schemas import (
    ChangeProductStatusRequest,
    ProductResponse,
)
from app.modules.products.services import change_product_status
from app.shared.base.enums import RoleName

router = APIRouter()


@router.patch(
    "/{product_id}/status",
    response_model=ProductResponse,
)
def change_product_status_endpoint(
    product_id: int,
    request: ChangeProductStatusRequest,
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
    return change_product_status(
        db=db,
        tenant_id=current_user.tenant_id,
        product_id=product_id,
        request=request,
    )