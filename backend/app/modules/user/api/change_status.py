from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import ChangeUserStatusRequest, UserResponse
from app.modules.user.services.change_status import ChangeUserStatusService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
def change_user_status(
    user_id: int,
    request: ChangeUserStatusRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles([RoleName.TENANT_ADMIN.value])
    ),
):
    repository = UserRepository(db)
    service = ChangeUserStatusService(repository)

    return service.change_status(
        user_id=user_id,
        request=request,
        current_user=current_user,
    )