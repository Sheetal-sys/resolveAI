import os
from collections.abc import Generator
from pathlib import Path
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# ---------------------------------------------------------
# Load test environment before importing the application.
# ---------------------------------------------------------

BACKEND_ROOT = Path(__file__).resolve().parent.parent
TEST_ENV_FILE = BACKEND_ROOT / ".env.test"

load_dotenv(
    dotenv_path=TEST_ENV_FILE,
    override=True,
)

TEST_DATABASE_URL = os.getenv("DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing from backend/.env.test"
    )

if "resolveai_test_db" not in TEST_DATABASE_URL:
    raise RuntimeError(
        "Tests must use resolveai_test_db, not the development database"
    )


# ---------------------------------------------------------
# Import application objects after loading .env.test.
# ---------------------------------------------------------

from app.database.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

# Import every model so it is registered in Base.metadata.
from app.modules.customer.models import Customer  # noqa: E402, F401
from app.modules.role.models import Role  # noqa: E402, F401
from app.modules.tenant.models import Tenant, TenantUser  # noqa: E402, F401
from app.modules.tenant_settings.models import TenantSettings  # noqa: E402, F401
from app.modules.user.models import User  # noqa: E402, F401
from app.modules.products.models import Product  # noqa: E402, F401

from tests.fixtures.auth import (  # noqa: E402, F401
    second_tenant_admin_context,
    second_tenant_admin_headers,
    second_tenant_admin_token,
    support_agent_context,
    support_agent_headers,
    support_agent_role,
    support_agent_token,
    tenant_admin_context,
    tenant_admin_headers,
    tenant_admin_role,
    tenant_admin_token,
)


# ---------------------------------------------------------
# Test database engine and session factory
# ---------------------------------------------------------

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ---------------------------------------------------------
# Test database lifecycle
# ---------------------------------------------------------

@pytest.fixture(
    scope="session",
    autouse=True,
)
def prepare_test_database() -> Generator[None, None, None]:
    """
    Recreate all test tables once at the start of the pytest session.

    This operates only against resolveai_test_db.
    """

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


# ---------------------------------------------------------
# Database session fixture
# ---------------------------------------------------------

@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """
    Provide a database session to one test.

    After the test, close the session and remove all inserted data.
    """

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()

        table_names = [
            table.name
            for table in reversed(Base.metadata.sorted_tables)
        ]

        if table_names:
            quoted_tables = ", ".join(
                f'"{table_name}"'
                for table_name in table_names
            )

            with test_engine.begin() as connection:
                connection.execute(
                    text(
                        f"TRUNCATE TABLE {quoted_tables} "
                        "RESTART IDENTITY CASCADE"
                    )
                )


# ---------------------------------------------------------
# FastAPI client fixture
# ---------------------------------------------------------

@pytest.fixture()
def client(
    db_session: Session,
) -> Generator[TestClient, None, None]:
    """
    Override the normal application database dependency.

    Every API request made through this client uses resolveai_test_db.
    """

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()