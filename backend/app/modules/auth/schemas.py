from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


class CurrentUserResponse(BaseModel):
    user_id: int
    email: str
    first_name: str
    last_name: str | None
    tenant_id: int
    tenant_name: str
    role: str