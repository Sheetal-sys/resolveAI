from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.services.remove_user import RemoveUserService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles([RoleName.TENANT_ADMIN.value])
    ),
):
    repository = UserRepository(db)
    service = RemoveUserService(repository)

    return service.remove_user(
        user_id=user_id,
        current_user=current_user,
    )