import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def create_order_data(client: TestClient):
    """Create a customer, product and order under the supplied tenant headers."""
    counter = 0

    def _create(headers: dict[str, str]) -> dict:
        nonlocal counter
        counter += 1
        suffix = f"{counter}-{id(headers)}"
        customer = client.post(
            "/api/v1/customers/", headers=headers,
            json={"first_name": "Orders", "last_name": "Tester",
                  "email": f"orders-{suffix}@example.com", "source": "WEBSITE"},
        )
        assert customer.status_code == 201, customer.text
        product = client.post(
            "/api/v1/products/", headers=headers,
            json={"sku": f"ORDERS-{suffix}", "name": "Order Test Product",
                  "price": "100.00", "currency": "USD", "stock_quantity": 20},
        )
        assert product.status_code == 201, product.text
        order = client.post(
            "/api/v1/orders/", headers=headers,
            json={"customer_id": customer.json()["id"], "currency": "USD",
                  "items": [{"product_id": product.json()["id"],
                             "quantity": 2, "unit_price": "100.00"}]},
        )
        assert order.status_code == 201, order.text
        return {"customer_id": customer.json()["id"],
                "product_id": product.json()["id"], "order": order.json()}

    return _create
