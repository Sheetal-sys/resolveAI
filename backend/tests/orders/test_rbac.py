from fastapi.testclient import TestClient


def test_support_agent_can_read_order(client: TestClient, tenant_admin_headers, support_agent_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.get(f'/api/v1/orders/{order["id"]}', headers=support_agent_headers)
    assert response.status_code == 200, response.text


def test_support_agent_cannot_create_order(client: TestClient, tenant_admin_headers, support_agent_headers, create_order_data):
    data = create_order_data(tenant_admin_headers)
    response = client.post('/api/v1/orders/', headers=support_agent_headers,
                           json={"customer_id": data["customer_id"], "items": [
                               {"product_id": data["product_id"], "quantity": 1, "unit_price": "100.00"}]})
    assert response.status_code == 403, response.text


def test_support_agent_cannot_update_order(client: TestClient, tenant_admin_headers, support_agent_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}', headers=support_agent_headers,
                            json={"tax_amount": "1.00"})
    assert response.status_code == 403, response.text
