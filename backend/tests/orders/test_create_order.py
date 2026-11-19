
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.modules.orders.models import Order, OrderItem


def test_tenant_admin_can_create_order(
    client: TestClient,
    db_session: Session,
    tenant_admin_headers: dict[str, str],
) -> None:
    # Step 1: Create a customer
    customer_response = client.post(
        "/api/v1/customers/",
        headers=tenant_admin_headers,
        json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "order.customer@test.com",
            "phone": "+919876543210",
            "source": "WEBSITE",
        },
    )

    assert customer_response.status_code == 201, customer_response.text

    customer_id = customer_response.json()["id"]

    # Step 2: Create a product
    product_response = client.post(
        "/api/v1/products/",
        headers=tenant_admin_headers,
        json={
            "sku": "ORDER-TEST-001",
            "name": "Test Laptop",
            "description": "Laptop for order integration testing",
            "category": "Electronics",
            "brand": "ResolveTech",
            "price": "500.00",
            "currency": "USD",
            "stock_quantity": 10,
        },
    )

    assert product_response.status_code == 201, product_response.text

    product_id = product_response.json()["id"]

    # Step 3: Create an order
    order_response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": customer_id,
            "currency": "USD",
            "tax_amount": "50.00",
            "shipping_amount": "20.00",
            "discount_amount": "100.00",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": "500.00",
                }
            ],
        },
    )

    assert order_response.status_code == 201, order_response.text

    data = order_response.json()

    # Step 4: Verify response
    assert data["status"] == "PENDING"
    assert data["order_number"].startswith("ORD-")
    assert Decimal(str(data["subtotal"])) == Decimal("1000.00")
    assert Decimal(str(data["total_amount"])) == Decimal("970.00")

    # Step 5: Verify database persistence
    order = (
        db_session.query(Order)
        .filter(Order.id == data["id"])
        .first()
    )

    assert order is not None
    assert order.customer_id == customer_id
    assert order.total_amount == Decimal("970.00")

    items = (
        db_session.query(OrderItem)
        .filter(OrderItem.order_id == order.id)
        .all()
    )

    assert len(items) == 1
    assert items[0].product_id == product_id
    assert items[0].quantity == 2
    assert items[0].line_total == Decimal("1000.00")



def test_order_without_items_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": 1,
            "currency": "USD",
            "tax_amount": "0.00",
            "shipping_amount": "0.00",
            "discount_amount": "0.00",
            "items": [],
        },
    )

    assert response.status_code == 422, response.text


def test_order_with_zero_quantity_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": 1,
            "currency": "USD",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 0,
                    "unit_price": "500.00",
                }
            ],
        },
    )

    assert response.status_code == 422, response.text



def test_order_with_negative_unit_price_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": 1,
            "currency": "USD",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "unit_price": "-500.00",
                }
            ],
        },
    )

    assert response.status_code == 422, response.text


def test_order_with_negative_tax_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": 1,
            "currency": "USD",
            "tax_amount": "-50.00",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "unit_price": "500.00",
                }
            ],
        },
    )

    assert response.status_code == 422, response.text



def test_order_with_negative_shipping_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": 1,
            "currency": "USD",
            "shipping_amount": "-20.00",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "unit_price": "500.00",
                }
            ],
        },
    )

    assert response.status_code == 422, response.text


def test_order_with_negative_discount_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": 1,
            "currency": "USD",
            "discount_amount": "-100.00",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "unit_price": "500.00",
                }
            ],
        },
    )

    assert response.status_code == 422, response.text



def test_order_with_nonexistent_customer_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/orders/",
        headers=tenant_admin_headers,
        json={
            "customer_id": 999999,
            "currency": "USD",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "unit_price": "500.00",
                }
            ],
        },
    )

    assert response.status_code == 404, response.text
