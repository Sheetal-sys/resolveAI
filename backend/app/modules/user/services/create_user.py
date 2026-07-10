from fastapi import HTTPException, status

from app.core.security import hash_password
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.models import User
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import UserCreateRequest, UserResponse
from app.shared.base.enums import RoleName


class CreateUserService:
    ALLOWED_EMPLOYEE_ROLES = {
        RoleName.SUPERVISOR.value,
        RoleName.SUPPORT_AGENT.value,
    }

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(
        self,
        request: UserCreateRequest,
        current_user: CurrentUserResponse,
    ) -> UserResponse:
        normalized_email = request.email.lower().strip()
        requested_role = request.role.upper().strip()

        if requested_role not in self.ALLOWED_EMPLOYEE_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid employee role. Allowed roles are "
                    "SUPERVISOR and SUPPORT_AGENT."
                ),
            )

        existing_user = self.repository.get_user_by_email(
            normalized_email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists",
            )

        role = self.repository.get_role_by_name(requested_role)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    f"Role {requested_role} was not found. "
                    "Please verify the role seed data."
                ),
            )

        try:
            user = User(
                first_name=request.first_name.strip(),
                last_name=(
                    request.last_name.strip()
                    if request.last_name
                    else None
                ),
                email=normalized_email,
                password_hash=hash_password(
                    request.temporary_password
                ),
                is_active=True,
            )

            user = self.repository.create_user(user)

            tenant_user = self.repository.create_tenant_user(
                tenant_id=current_user.tenant_id,
                user_id=user.id,
                role_id=role.id,
            )

            self.repository.commit()

            self.repository.refresh(user)
            self.repository.refresh(tenant_user)

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

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User creation failed: {str(exc)}",
            ) from exc