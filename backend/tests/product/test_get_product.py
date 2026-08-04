from fastapi.testclient import TestClient


def create_product(
    client: TestClient,
    headers: dict[str, str],
    *,
    sku: str = "GET-001",
    name: str = "Get Product",
) -> dict:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "sku": sku,
            "name": name,
            "description": "Created for get-product test",
            "category": "Electronics",
            "brand": "ResolveTech",
            "price": 1499.99,
            "currency": "INR",
            "stock_quantity": 12,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_get_existing_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
    )

    response = client.get(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == product["id"]
    assert data["product_code"] == product["product_code"]
    assert data["sku"] == "GET-001"
    assert data["name"] == "Get Product"
    assert data["status"] == "ACTIVE"


def test_get_unknown_product_returns_404(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.get(
        "/api/v1/products/999999",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }