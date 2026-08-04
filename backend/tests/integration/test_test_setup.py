from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session


def test_test_database_is_available(
    db_session: Session,
) -> None:
    result = db_session.execute(
        text("SELECT current_database()")
    )

    database_name = result.scalar_one()

    assert database_name == "resolveai_test_db"


def test_fastapi_test_client_is_available(
    client: TestClient,
) -> None:
    response = client.get("/health")

    assert response.status_code == 200