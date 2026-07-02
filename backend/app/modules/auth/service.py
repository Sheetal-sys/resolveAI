from fastapi import HTTPException, status

from app.core.security import create_access_token, decode_access_token, verify_password
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import CurrentUserResponse, LoginRequest, LoginResponse


class AuthService:

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def login(self, request: LoginRequest) -> LoginResponse:
        user = self.repository.get_user_by_email(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return LoginResponse(
            access_token=access_token,
            user_id=user.id,
            email=user.email,
        )

    def get_current_user(self, token: str) -> CurrentUserResponse:
        try:
            payload = decode_access_token(token)
            subject = payload.get("sub")

            if subject is None:
             raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token payload",
    )

            user_id = int(subject)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        user = self.repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        tenant_role_data = self.repository.get_user_tenant_role(user.id)

        if not tenant_role_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not assigned to any tenant",
            )

        tenant_user, tenant, role = tenant_role_data

        return CurrentUserResponse(
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            tenant_id=tenant.id,
            tenant_name=tenant.name,
            role=role.name,
        )