from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.products.schemas import ProductResponse
from app.modules.products.services import get_product
from app.shared.base.enums import RoleName

router = APIRouter()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product_endpoint(
    product_id: int,
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
    return get_product(
        db=db,
        tenant_id=current_user.tenant_id,
        product_id=product_id,
    )