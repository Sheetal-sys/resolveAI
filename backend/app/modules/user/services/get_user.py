from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import UserResponse


class GetUserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(
        self,
        user_id: int,
        current_user: CurrentUserResponse,
    ) -> UserResponse:

        record = self.repository.get_user_by_id_and_tenant(
            user_id=user_id,
            tenant_id=current_user.tenant_id,
        )

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user, tenant_user, role = record

        return UserResponse(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=role.name,
            is_active=tenant_user.is_active,
            tenant_id=tenant_user.tenant_id,
            joined_at=tenant_user.joined_at,
        )