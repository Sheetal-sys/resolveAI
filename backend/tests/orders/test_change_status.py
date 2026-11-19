from fastapi.testclient import TestClient


def test_valid_order_status_transition(client: TestClient, tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}/status', headers=tenant_admin_headers,
                            json={"status": "CONFIRMED"})
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "CONFIRMED"


def test_invalid_order_status_transition_returns_409(client: TestClient, tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}/status', headers=tenant_admin_headers,
                            json={"status": "DELIVERED"})
    assert response.status_code == 409, response.text


def test_duplicate_order_status_returns_409(client: TestClient, tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}/status', headers=tenant_admin_headers,
                            json={"status": "PENDING"})
    assert response.status_code == 409, response.text


def test_shipped_order_cannot_be_financially_updated(client: TestClient, tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    for state in ("CONFIRMED", "PROCESSING", "SHIPPED"):
        response = client.patch(f'/api/v1/orders/{order["id"]}/status', headers=tenant_admin_headers,
                                json={"status": state})
        assert response.status_code == 200, response.text
    update = client.patch(f'/api/v1/orders/{order["id"]}', headers=tenant_admin_headers,
                          json={"tax_amount": "15.00"})
    assert update.status_code == 409, update.text
