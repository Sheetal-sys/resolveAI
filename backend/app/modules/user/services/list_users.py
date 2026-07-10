from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import UserListResponse, UserResponse


class ListUsersService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def list_users(
        self,
        current_user: CurrentUserResponse,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> UserListResponse:
        records, total = self.repository.list_users_by_tenant(
            tenant_id=current_user.tenant_id,
            skip=skip,
            limit=limit,
            search=search,
        )

        items = [
            UserResponse(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=role.name,
                is_active=tenant_user.is_active,
                tenant_id=tenant_user.tenant_id,
                joined_at=tenant_user.joined_at,
            )
            for user, tenant_user, role in records
        ]

        return UserListResponse(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
        )