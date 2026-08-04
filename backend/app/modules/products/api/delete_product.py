from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.products.services import delete_product
from app.shared.base.enums import RoleName

router = APIRouter()


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
)
def delete_product_endpoint(
    product_id: int,
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
    return delete_product(
        db=db,
        tenant_id=current_user.tenant_id,
        product_id=product_id,
    )