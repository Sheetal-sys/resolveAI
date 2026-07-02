from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import CurrentUserResponse, LoginRequest, LoginResponse
from app.modules.auth.service import AuthService
from app.modules.auth.dependencies import require_roles

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)

security = HTTPBearer()


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    repository = AuthRepository(db)
    service = AuthService(repository)

    return service.login(request)


@router.get("/me", response_model=CurrentUserResponse)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    repository = AuthRepository(db)
    service = AuthService(repository)

    return service.get_current_user(credentials.credentials)

@router.get("/admin-test")
def admin_test(
    current_user=Depends(require_roles(["TENANT_ADMIN"])),
):
    return {
        "message": "You are allowed to access tenant admin area",
        "user_id": current_user.user_id,
        "role": current_user.role,
        "tenant_id": current_user.tenant_id,
    }