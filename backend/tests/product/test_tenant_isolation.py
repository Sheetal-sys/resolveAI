from fastapi.testclient import TestClient


def create_product(
    client: TestClient,
    headers: dict[str, str],
    *,
    sku: str,
    name: str,
) -> dict:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "sku": sku,
            "name": name,
            "description": f"{name} description",
            "category": "Electronics",
            "brand": "ResolveTech",
            "price": 999.99,
            "currency": "INR",
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_tenant_cannot_get_another_tenants_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        second_tenant_admin_headers,
        sku="SECOND-GET-001",
        name="Second Tenant Product",
    )

    response = client.get(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_tenant_cannot_update_another_tenants_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        second_tenant_admin_headers,
        sku="SECOND-UPDATE-001",
        name="Second Tenant Product",
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
        json={
            "name": "Unauthorized Update",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_tenant_cannot_change_another_tenants_product_status(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        second_tenant_admin_headers,
        sku="SECOND-STATUS-001",
        name="Second Tenant Product",
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}/status",
        headers=tenant_admin_headers,
        json={
            "status": "INACTIVE",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_tenant_cannot_delete_another_tenants_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        second_tenant_admin_headers,
        sku="SECOND-DELETE-001",
        name="Second Tenant Product",
    )

    response = client.delete(
        f"/api/v1/products/{product['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_product_list_contains_only_authenticated_tenant_data(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    create_product(
        client,
        tenant_admin_headers,
        sku="FIRST-LIST-001",
        name="First Tenant Product",
    )

    create_product(
        client,
        second_tenant_admin_headers,
        sku="SECOND-LIST-001",
        name="Second Tenant Product",
    )

    first_response = client.get(
        "/api/v1/products/",
        headers=tenant_admin_headers,
    )

    second_response = client.get(
        "/api/v1/products/",
        headers=second_tenant_admin_headers,
    )

    assert first_response.status_code == 200, first_response.text
    assert second_response.status_code == 200, second_response.text

    first_data = first_response.json()
    second_data = second_response.json()

    assert first_data["total"] == 1
    assert first_data["items"][0]["sku"] == "FIRST-LIST-001"

    assert second_data["total"] == 1
    assert second_data["items"][0]["sku"] == "SECOND-LIST-001"


def test_same_sku_is_allowed_for_different_tenants(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    first_product = create_product(
        client,
        tenant_admin_headers,
        sku="SHARED-SKU-001",
        name="First Tenant Product",
    )

    second_product = create_product(
        client,
        second_tenant_admin_headers,
        sku="SHARED-SKU-001",
        name="Second Tenant Product",
    )

    assert first_product["sku"] == "SHARED-SKU-001"
    assert second_product["sku"] == "SHARED-SKU-001"
    assert first_product["id"] != second_product["id"]