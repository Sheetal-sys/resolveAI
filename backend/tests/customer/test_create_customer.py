from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.modules.customer.models import Customer


def test_tenant_admin_can_create_customer(
    client: TestClient,
    db_session: Session,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/customers/",
        headers=tenant_admin_headers,
        json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@test.com",
            "phone": "+919876543210",
            "company": "Test Company",
            "source": "WEBSITE",
            "internal_notes": "Created through integration test",
        },
    )

    assert response.status_code == 201, response.text

    response_data = response.json()

    assert response_data["first_name"] == "John"
    assert response_data["last_name"] == "Smith"
    assert response_data["email"] == "john.smith@test.com"
    assert response_data["status"] == "ACTIVE"
    assert response_data["source"] == "WEBSITE"
    assert response_data["customer_code"].startswith("CUST-")

    customer = (
        db_session.query(Customer)
        .filter(Customer.email == "john.smith@test.com")
        .first()
    )

    assert customer is not None
    assert customer.first_name == "John"
    assert customer.tenant_id is not None

def test_duplicate_customer_email_is_rejected(
    client: TestClient,
    db_session: Session,
    tenant_admin_headers: dict[str, str],
) -> None:
    payload = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "duplicate@test.com",
        "phone": "+919876543210",
        "company": "Test Company",
        "source": "WEBSITE",
    }

    first_response = client.post(
        "/api/v1/customers/",
        headers=tenant_admin_headers,
        json=payload,
    )

    assert first_response.status_code == 201, first_response.text

    second_response = client.post(
        "/api/v1/customers/",
        headers=tenant_admin_headers,
        json=payload,
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "A customer with this email already exists"
    }    