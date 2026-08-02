from datetime import time

from pydantic import BaseModel, EmailStr, Field, HttpUrl, model_validator


class UpdateTenantSettingsRequest(BaseModel):
    website: HttpUrl | None = None
    support_email: EmailStr | None = None
    support_phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=30,
    )

    timezone: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    language: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    business_start_time: time | None = None
    business_end_time: time | None = None

    logo_url: HttpUrl | None = None

    ai_confidence_threshold: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    auto_reply: bool | None = None
    auto_escalation: bool | None = None

    @model_validator(mode="after")
    def validate_business_hours(self):
        if (
            self.business_start_time is not None
            and self.business_end_time is not None
            and self.business_start_time >= self.business_end_time
        ):
            raise ValueError(
                "business_start_time must be earlier than business_end_time"
            )

        return self