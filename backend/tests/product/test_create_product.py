from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.modules.products.models import Product


def test_tenant_admin_can_create_product(
    client: TestClient,
    db_session: Session,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/products/",
        headers=tenant_admin_headers,
        json={
            "sku": "LAPTOP-001",
            "name": "ProBook Laptop",
            "description": "15-inch business laptop",
            "category": "Electronics",
            "brand": "ResolveTech",
            "price": 74999.99,
            "currency": "INR",
            "stock_quantity": 25,
            "image_url": "https://example.com/images/probook-laptop.png",
        },
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["sku"] == "LAPTOP-001"
    assert data["name"] == "ProBook Laptop"
    assert data["price"] == "74999.99"
    assert data["currency"] == "INR"
    assert data["stock_quantity"] == 25
    assert data["status"] == "ACTIVE"
    assert data["product_code"].startswith("PROD-")

    product = (
        db_session.query(Product)
        .filter(Product.sku == "LAPTOP-001")
        .first()
    )

    assert product is not None
    assert product.name == "ProBook Laptop"
    assert product.tenant_id is not None


def test_duplicate_product_sku_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    payload = {
        "sku": "DUPLICATE-001",
        "name": "Duplicate Product",
        "description": "Duplicate SKU test",
        "category": "Electronics",
        "brand": "ResolveTech",
        "price": 999.99,
        "currency": "INR",
        "stock_quantity": 10,
    }

    first_response = client.post(
        "/api/v1/products/",
        headers=tenant_admin_headers,
        json=payload,
    )

    assert first_response.status_code == 201, first_response.text

    second_response = client.post(
        "/api/v1/products/",
        headers=tenant_admin_headers,
        json=payload,
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "A product with this SKU already exists.",
    }


def test_negative_product_price_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/products/",
        headers=tenant_admin_headers,
        json={
            "sku": "NEGATIVE-PRICE-001",
            "name": "Invalid Product",
            "price": -10,
            "currency": "INR",
            "stock_quantity": 5,
        },
    )

    assert response.status_code == 422


def test_negative_stock_quantity_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/products/",
        headers=tenant_admin_headers,
        json={
            "sku": "NEGATIVE-STOCK-001",
            "name": "Invalid Stock Product",
            "price": 100,
            "currency": "INR",
            "stock_quantity": -1,
        },
    )

    assert response.status_code == 422