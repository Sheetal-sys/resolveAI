from fastapi.testclient import TestClient


def test_get_existing_order(client: TestClient, tenant_admin_headers, create_order_data):
    created = create_order_data(tenant_admin_headers)["order"]
    response = client.get(f'/api/v1/orders/{created["id"]}', headers=tenant_admin_headers)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == created["id"]
    assert len(response.json()["items"]) == 1


def test_get_unknown_order_returns_404(client: TestClient, tenant_admin_headers):
    response = client.get('/api/v1/orders/999999', headers=tenant_admin_headers)
    assert response.status_code == 404, response.text


def test_list_orders_filters_by_customer_and_paginates(client: TestClient, tenant_admin_headers, create_order_data):
    first = create_order_data(tenant_admin_headers)
    second = create_order_data(tenant_admin_headers)
    response = client.get('/api/v1/orders/', headers=tenant_admin_headers,
                          params={"customer_id": first["customer_id"], "skip": 0, "limit": 1})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["total"] == 1
    assert data["skip"] == 0 and data["limit"] == 1
    assert [item["id"] for item in data["items"]] == [first["order"]["id"]]
    assert second["order"]["id"] not in [item["id"] for item in data["items"]]
