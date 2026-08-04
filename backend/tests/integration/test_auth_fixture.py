from fastapi.testclient import TestClient


def test_tenant_admin_can_login(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["email"] == "admin@testshop.com"
    assert response_data["tenant_name"] == "Test Shop"
    assert response_data["role"] == "TENANT_ADMIN"