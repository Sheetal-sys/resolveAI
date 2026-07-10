from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import UserListResponse
from app.modules.user.services.list_users import ListUsersService
from app.shared.base.enums import RoleName

router = APIRouter()


@router.get(
    "/",
    response_model=UserListResponse,
)
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, max_length=150),
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
    repository = UserRepository(db)
    service = ListUsersService(repository)

    return service.list_users(
        current_user=current_user,
        skip=skip,
        limit=limit,
        search=search,
    )