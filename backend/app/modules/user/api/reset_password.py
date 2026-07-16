from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import ResetUserPasswordRequest
from app.modules.user.services.reset_password import ResetUserPasswordService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.post("/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    request: ResetUserPasswordRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles([RoleName.TENANT_ADMIN.value])
    ),
):
    repository = UserRepository(db)
    service = ResetUserPasswordService(repository)

    return service.reset_password(
        user_id=user_id,
        request=request,
        current_user=current_user,
    )