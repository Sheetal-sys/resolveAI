from decimal import Decimal

from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.orders.models import Order, OrderItem
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderCreateRequest, OrderResponse
from app.modules.products.repository import ProductRepository
from app.shared.base.enums import OrderStatus


class CreateOrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
    ):
        self.order_repository = order_repository
        self.customer_repository = customer_repository
        self.product_repository = product_repository

    def create_order(
        self,
        request: OrderCreateRequest,
        current_user: CurrentUserResponse,
    ) -> OrderResponse:
        tenant_id = current_user.tenant_id

        # 1. Validate customer belongs to this tenant
        customer = self.customer_repository.get_by_id_and_tenant(
            customer_id=request.customer_id,
            tenant_id=tenant_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        # 2. Validate every product belongs to this tenant
        validated_products = {}
        for item_request in request.items:
            product = self.product_repository.get_by_id_and_tenant(
                product_id=item_request.product_id,
                tenant_id=tenant_id,
            )

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Product with id {item_request.product_id} not found"
                    ),
                )

            validated_products[item_request.product_id] = product

        # 3. Build order inside a single transaction
        try:
            # Create order with temporary order number
            order = Order(
                tenant_id=tenant_id,
                customer_id=request.customer_id,
                order_number="TEMP",
                status=OrderStatus.PENDING.value,
                currency=request.currency.upper().strip(),
                subtotal=Decimal("0.00"),
                tax_amount=request.tax_amount,
                shipping_amount=request.shipping_amount,
                discount_amount=request.discount_amount,
                total_amount=Decimal("0.00"),
            )

            order = self.order_repository.create(order)

            # Generate order number from PK
            order.order_number = f"ORD-{order.id:08d}"
            self.order_repository.update(order)

            # Create items and compute subtotal
            subtotal = Decimal("0.00")

            for item_request in request.items:
                # Backend-calculated line_total — never trust client
                line_total = (
                    item_request.unit_price * item_request.quantity
                ).quantize(Decimal("0.01"))

                subtotal += line_total

                order_item = OrderItem(
                    tenant_id=tenant_id,
                    order_id=order.id,
                    product_id=item_request.product_id,
                    quantity=item_request.quantity,
                    unit_price=item_request.unit_price,
                    line_total=line_total,
                )

                self.order_repository.create_item(order_item)

            # Backend-calculated total
            total_amount = (
                subtotal
                + request.tax_amount
                + request.shipping_amount
                - request.discount_amount
            ).quantize(Decimal("0.01"))

            order.subtotal = subtotal
            order.total_amount = total_amount
            self.order_repository.update(order)

            self.order_repository.commit()
            self.order_repository.refresh(order)

            return OrderResponse.model_validate(order)

        except HTTPException:
            self.order_repository.rollback()
            raise

        except Exception as exc:
            self.order_repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Order creation failed: {str(exc)}",
            ) from exc
