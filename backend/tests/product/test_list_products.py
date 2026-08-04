from fastapi.testclient import TestClient


def create_product(
    client: TestClient,
    headers: dict[str, str],
    *,
    sku: str,
    name: str,
    category: str = "Electronics",
    status: str = "ACTIVE",
) -> dict:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "sku": sku,
            "name": name,
            "description": f"{name} description",
            "category": category,
            "brand": "ResolveTech",
            "price": 999.99,
            "currency": "INR",
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201, response.text

    product = response.json()

    if status != "ACTIVE":
        status_response = client.patch(
            f"/api/v1/products/{product['id']}/status",
            headers=headers,
            json={"status": status},
        )

        assert status_response.status_code == 200, status_response.text

    return product


def test_tenant_admin_can_list_products(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_product(
        client,
        tenant_admin_headers,
        sku="LIST-001",
        name="Laptop",
    )

    create_product(
        client,
        tenant_admin_headers,
        sku="LIST-002",
        name="Phone",
    )

    response = client.get(
        "/api/v1/products/",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 2
    assert data["skip"] == 0
    assert data["limit"] == 20
    assert len(data["items"]) == 2


def test_product_list_supports_search(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_product(
        client,
        tenant_admin_headers,
        sku="SEARCH-001",
        name="Gaming Laptop",
    )

    create_product(
        client,
        tenant_admin_headers,
        sku="SEARCH-002",
        name="Office Chair",
        category="Furniture",
    )

    response = client.get(
        "/api/v1/products/?search=gaming",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Gaming Laptop"


def test_product_list_supports_pagination(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    for index in range(5):
        create_product(
            client,
            tenant_admin_headers,
            sku=f"PAGE-{index:03d}",
            name=f"Product {index}",
        )

    response = client.get(
        "/api/v1/products/?skip=1&limit=2",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 5
    assert data["skip"] == 1
    assert data["limit"] == 2
    assert len(data["items"]) == 2


def test_product_list_filters_by_status(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_product(
        client,
        tenant_admin_headers,
        sku="ACTIVE-001",
        name="Active Product",
        status="ACTIVE",
    )

    create_product(
        client,
        tenant_admin_headers,
        sku="INACTIVE-001",
        name="Inactive Product",
        status="INACTIVE",
    )

    response = client.get(
        "/api/v1/products/?product_status=INACTIVE",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["status"] == "INACTIVE"


def test_product_list_filters_by_category(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_product(
        client,
        tenant_admin_headers,
        sku="ELEC-001",
        name="Laptop",
        category="Electronics",
    )

    create_product(
        client,
        tenant_admin_headers,
        sku="FURN-001",
        name="Office Chair",
        category="Furniture",
    )

    response = client.get(
        "/api/v1/products/?category=Furniture",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["category"] == "Furniture"