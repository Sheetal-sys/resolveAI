from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProductCreateRequest(BaseModel):
    sku: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    category: str | None = Field(
        default=None,
        max_length=100,
    )

    brand: str | None = Field(
        default=None,
        max_length=100,
    )

    price: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
    )

    currency: str = Field(
        default="USD",
        min_length=3,
        max_length=3,
    )

    stock_quantity: int = Field(
        default=0,
        ge=0,
    )

    image_url: HttpUrl | None = None


class ProductUpdateRequest(BaseModel):
    sku: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    category: str | None = Field(
        default=None,
        max_length=100,
    )

    brand: str | None = Field(
        default=None,
        max_length=100,
    )

    price: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    stock_quantity: int | None = Field(
        default=None,
        ge=0,
    )

    image_url: HttpUrl | None = None


class ChangeProductStatusRequest(BaseModel):
    status: str = Field(
        ...,
        pattern="^(ACTIVE|INACTIVE)$",
    )


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_code: str
    sku: str
    name: str
    description: str | None
    category: str | None
    brand: str | None
    price: Decimal
    currency: str
    stock_quantity: int
    status: str
    image_url: str | None
    created_at: datetime
    updated_at: datetime | None


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    skip: int
    limit: int