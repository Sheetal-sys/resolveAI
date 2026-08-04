from fastapi.testclient import TestClient


def create_product(
    client: TestClient,
    headers: dict[str, str],
    *,
    sku: str = "STATUS-001",
) -> dict:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "sku": sku,
            "name": "Status Product",
            "description": "Created for status tests",
            "category": "Electronics",
            "brand": "ResolveTech",
            "price": 1499.99,
            "currency": "INR",
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201, response.text
    return response.json()


def test_tenant_admin_can_deactivate_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}/status",
        headers=tenant_admin_headers,
        json={"status": "INACTIVE"},
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == product["id"]
    assert data["status"] == "INACTIVE"


def test_product_status_change_is_persisted(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="STATUS-PERSIST-001",
    )

    update_response = client.patch(
        f"/api/v1/products/{product['id']}/status",
        headers=tenant_admin_headers,
        json={"status": "INACTIVE"},
    )

    assert update_response.status_code == 200, update_response.text

    get_response = client.get(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert get_response.status_code == 200, get_response.text
    assert get_response.json()["status"] == "INACTIVE"


def test_duplicate_product_status_change_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="STATUS-DUPLICATE-001",
    )

    first_response = client.patch(
        f"/api/v1/products/{product['id']}/status",
        headers=tenant_admin_headers,
        json={"status": "INACTIVE"},
    )

    assert first_response.status_code == 200, first_response.text

    second_response = client.patch(
        f"/api/v1/products/{product['id']}/status",
        headers=tenant_admin_headers,
        json={"status": "INACTIVE"},
    )

    assert second_response.status_code == 400
    assert second_response.json() == {
        "detail": "Product is already INACTIVE",
    }


def test_change_status_for_unknown_product_returns_404(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.patch(
        "/api/v1/products/999999/status",
        headers=tenant_admin_headers,
        json={"status": "INACTIVE"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_invalid_product_status_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="STATUS-INVALID-001",
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}/status",
        headers=tenant_admin_headers,
        json={"status": "BLOCKED"},
    )

    assert response.status_code == 422