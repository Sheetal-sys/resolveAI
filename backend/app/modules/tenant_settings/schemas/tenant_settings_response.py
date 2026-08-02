from datetime import time

from pydantic import BaseModel, ConfigDict, EmailStr


class TenantSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tenant_id: int
    company_name: str

    website: str | None
    support_email: EmailStr | None
    support_phone: str | None

    timezone: str
    language: str
    currency: str

    business_start_time: time
    business_end_time: time

    logo_url: str | None

    ai_confidence_threshold: int
    auto_reply: bool
    auto_escalation: bool