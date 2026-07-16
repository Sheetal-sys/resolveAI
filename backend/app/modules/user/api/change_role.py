from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import ChangeUserRoleRequest, UserResponse
from app.modules.user.services.change_role import ChangeUserRoleService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
)
def change_user_role(
    user_id: int,
    request: ChangeUserRoleRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles([RoleName.TENANT_ADMIN.value])
    ),
):
    repository = UserRepository(db)
    service = ChangeUserRoleService(repository)

    return service.change_role(
        user_id=user_id,
        request=request,
        current_user=current_user,
    )