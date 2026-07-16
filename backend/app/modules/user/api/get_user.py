from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import UserResponse
from app.modules.user.services.get_user import GetUserService

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = GetUserService(repository)

    return service.get_user(
        user_id=user_id,
        current_user=current_user,
    )