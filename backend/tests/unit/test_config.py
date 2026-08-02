from app.core.config import settings


def test_application_settings_are_loaded() -> None:
    assert settings.APP_NAME == "ResolveAI"
    assert settings.DATABASE_URL
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0