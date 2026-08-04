from app.core.config import settings


def test_application_settings_are_loaded() -> None:
    assert settings.APP_NAME == "ResolveAI-Test"
    assert settings.APP_VERSION == "1.0.0"

    assert settings.DATABASE_URL
    assert "resolveai_test_db" in settings.DATABASE_URL

    assert settings.SECRET_KEY
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0