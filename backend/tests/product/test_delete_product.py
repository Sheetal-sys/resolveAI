from fastapi.testclient import TestClient


def create_product(
    client: TestClient,
    headers: dict[str, str],
    *,
    sku: str = "DELETE-001",
) -> dict:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "sku": sku,
            "name": "Delete Product",
            "description": "Created for delete tests",
            "category": "Electronics",
            "brand": "ResolveTech",
            "price": 1499.99,
            "currency": "INR",
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_tenant_admin_can_delete_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
    )

    response = client.delete(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Product deleted successfully",
    }


def test_deleted_product_is_no_longer_available(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="DELETE-LOOKUP-001",
    )

    delete_response = client.delete(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert delete_response.status_code == 200, delete_response.text

    get_response = client.get(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Product not found",
    }


def test_delete_unknown_product_returns_404(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.delete(
        "/api/v1/products/999999",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_deleted_product_does_not_appear_in_list(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    first_product = create_product(
        client,
        tenant_admin_headers,
        sku="DELETE-FIRST-001",
    )

    second_product = create_product(
        client,
        tenant_admin_headers,
        sku="DELETE-SECOND-001",
    )

    delete_response = client.delete(
        f"/api/v1/products/{first_product['id']}",
        headers=tenant_admin_headers,
    )

    assert delete_response.status_code == 200, delete_response.text

    list_response = client.get(
        "/api/v1/products/",
        headers=tenant_admin_headers,
    )

    assert list_response.status_code == 200, list_response.text

    data = list_response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == second_product["id"]