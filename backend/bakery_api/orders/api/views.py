from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer
from customers.models import Customer
from django.db import transaction
from decimal import Decimal

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Lấy dữ liệu từ request
            user_id = request.data.get('user_id')
            is_logged_in = request.data.get('isLoggedIn', False)
            total_amount = Decimal(request.data.get('total_amount', 0))
            discount = Decimal(request.data.get('discount', 0))
            final_amount = Decimal(request.data.get('final_amount', 0))
            payment_method = request.data.get('payment_method')
            customer_name = request.data.get('customer_name')
            customer_phone = request.data.get('customer_phone')
            customer_email = request.data.get('customer_email')
            address = request.data.get('address')
            items = request.data.get('items', [])

            # Xử lý Customer
            customer = None
            if is_logged_in and user_id:
                # Người dùng đã đăng nhập
                try:
                    customer = Customer.objects.get(user_id=user_id)
                    # Kiểm tra thông tin Customer
                    # if not customer.name and not customer.phone and not customer.email and not customer.address:
                        # Cập nhật thông tin từ form
                    customer.name = customer_name
                    customer.phone = customer_phone
                    customer.email = customer_email
                    customer.address = address
                    customer.loyalty_point += int(final_amount * Decimal('0.01'))
                    customer.save()
                    # else:
                    #     # Cập nhật loyalty_point = 10% final_amount
                    #     customer.loyalty_point += int(final_amount * Decimal('0.01'))
                    #     customer.save()
                except Customer.DoesNotExist:
                    return Response({"message": "Customer not found for this user"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Khách vãn lai: Tạo Customer mới
                customer = Customer.objects.create(
                    name=customer_name,
                    phone=customer_phone,
                    email=customer_email,
                    address=address,
                    loyalty_point=0,
                    user=None  # Không liên kết với User
                )

            # Tạo Order
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount,
                discount=discount,
                final_amount=final_amount,
                payment_method=payment_method
            )

            # Tạo OrderDetail
            for item in items:
                OrderDetail.objects.create(
                    order=order,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    sub_total=item['sub_total']
                )

            # Trả về phản hồi
            return Response({
                "order_id": order.order_id,
                "customer_id": customer.customer_id,
                "loyalty_point": customer.loyalty_point,
                "message": "Order created successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": f"Error creating order: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_processed = request.data.get('is_processed')

        if is_processed is not None:
            order_details = OrderDetail.objects.filter(order=instance)
            if is_processed:  # Tick xử lý
                for detail in order_details:
                    product = detail.product
                    if product.stock_quantity < detail.quantity:
                        raise ValidationError({
                            'error': f'Sản phẩm {product.name} không đủ hàng (còn {product.stock_quantity}, cần {detail.quantity})'
                        })
                    product.stock_quantity -= detail.quantity
                    product.save()
            else:  # Bỏ tick xử lý
                for detail in order_details:
                    product = detail.product
                    product.stock_quantity += detail.quantity
                    product.save()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset