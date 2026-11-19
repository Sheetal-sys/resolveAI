from decimal import Decimal
from fastapi.testclient import TestClient


def test_update_order_recalculates_total(client: TestClient, tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}', headers=tenant_admin_headers,
                            json={"tax_amount": "10.00", "shipping_amount": "5.00", "discount_amount": "20.00"})
    assert response.status_code == 200, response.text
    assert Decimal(str(response.json()["total_amount"])) == Decimal("195.00")
    persisted = client.get(f'/api/v1/orders/{order["id"]}', headers=tenant_admin_headers)
    assert Decimal(str(persisted.json()["total_amount"])) == Decimal("195.00")


def test_empty_order_update_is_rejected(client: TestClient, tenant_admin_headers, create_order_data):
    order = create_order_data(tenant_admin_headers)["order"]
    response = client.patch(f'/api/v1/orders/{order["id"]}', headers=tenant_admin_headers, json={})
    assert response.status_code == 400, response.text
