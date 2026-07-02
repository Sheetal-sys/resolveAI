from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TenantRegisterRequest(BaseModel):
    company_name: str = Field(..., min_length=3, max_length=150)
    company_slug: str = Field(..., min_length=3, max_length=100)

    admin_first_name: str = Field(..., min_length=2, max_length=100)
    admin_last_name: str | None = Field(default=None, max_length=100)

    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8)


class TenantRegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tenant_id: int
    company_name: str
    company_slug: str
    admin_email: str
    message: str