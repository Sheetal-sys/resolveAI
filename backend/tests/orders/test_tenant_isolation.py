from fastapi.testclient import TestClient


def test_other_tenant_cannot_get_order(client: TestClient, tenant_admin_headers, second_tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.get(f'/api/v1/orders/{order["id"]}', headers=second_tenant_admin_headers)
    assert response.status_code == 404, response.text


def test_other_tenant_cannot_update_order(client: TestClient, tenant_admin_headers, second_tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}', headers=second_tenant_admin_headers,
                            json={"tax_amount": "5.00"})
    assert response.status_code == 404, response.text


def test_other_tenant_cannot_change_order_status(client: TestClient, tenant_admin_headers, second_tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}/status', headers=second_tenant_admin_headers,
                            json={"status": "CONFIRMED"})
    assert response.status_code == 404, response.text


def test_other_tenant_cannot_see_order_in_list(client: TestClient, tenant_admin_headers, second_tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.get('/api/v1/orders/', headers=second_tenant_admin_headers)
    assert response.status_code == 200, response.text
    assert order["id"] not in [item["id"] for item in response.json()["items"]]
