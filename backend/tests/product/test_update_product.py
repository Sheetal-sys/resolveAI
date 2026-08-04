from fastapi.testclient import TestClient


def create_product(
    client: TestClient,
    headers: dict[str, str],
    *,
    sku: str = "UPDATE-001",
) -> dict:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "sku": sku,
            "name": "Original Product",
            "description": "Original description",
            "category": "Electronics",
            "brand": "Original Brand",
            "price": 1999.99,
            "currency": "INR",
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_tenant_admin_can_update_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
        json={
            "name": "Updated Product",
            "description": "Updated description",
            "brand": "Updated Brand",
            "price": 2499.99,
            "currency": "usd",
            "stock_quantity": 25,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == product["id"]
    assert data["name"] == "Updated Product"
    assert data["description"] == "Updated description"
    assert data["brand"] == "Updated Brand"
    assert data["price"] == "2499.99"
    assert data["currency"] == "USD"
    assert data["stock_quantity"] == 25

    # These fields must remain unchanged.
    assert data["sku"] == "UPDATE-001"
    assert data["product_code"] == product["product_code"]
    assert data["status"] == "ACTIVE"


def test_product_update_is_persisted(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="PERSIST-001",
    )

    update_response = client.patch(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
        json={
            "category": "Office Equipment",
        },
    )

    assert update_response.status_code == 200, update_response.text

    get_response = client.get(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert get_response.status_code == 200, get_response.text
    assert get_response.json()["category"] == "Office Equipment"


def test_update_unknown_product_returns_404(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.patch(
        "/api/v1/products/999999",
        headers=tenant_admin_headers,
        json={
            "name": "Unknown Product",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_empty_product_update_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="EMPTY-UPDATE-001",
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
        json={},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "No fields were provided for update",
    }


def test_duplicate_product_sku_update_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    first_product = create_product(
        client,
        tenant_admin_headers,
        sku="FIRST-SKU-001",
    )

    second_product = create_product(
        client,
        tenant_admin_headers,
        sku="SECOND-SKU-001",
    )

    response = client.patch(
        f"/api/v1/products/{second_product['id']}",
        headers=tenant_admin_headers,
        json={
            "sku": first_product["sku"],
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "A product with this SKU already exists.",
    }