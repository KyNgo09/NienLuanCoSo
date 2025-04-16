from django.shortcuts import render
from rest_framework import viewsets, status
from orders.models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer
from customers.models import Customer
from accounts.models import User
from products.models import Product
from customers.api.serializers import CustomerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
import logging
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_order(request):
    logger.info("Received order creation request")
    
    try:
        data = request.data
        logger.debug(f"Request data: {data}")

        # Validate required fields
        if not data.get('customer_phone') or not data.get('customer_name'):
            logger.error("Missing required customer fields")
            return Response({'error': 'Tên và số điện thoại là bắt buộc'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        if not data.get('items') or len(data['items']) == 0:
            logger.error("Empty items in order")
            return Response({'error': 'Giỏ hàng không thể trống'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Xử lý khách hàng
            if data.get('isLoggedIn') and data.get('user_id'):
                try:
                    user = User.objects.get(pk=data['user_id'])
                    customer, created = Customer.objects.get_or_create(
                        user=user,
                        defaults={
                            'name': data['customer_name'],
                            'phone': data['customer_phone'],
                            'email': data.get('customer_email', ''),
                            'address': data.get('address', ''),
                            'loyalty_point': 0
                        }
                    )
                    logger.info(f"Existing customer found: {customer.customer_id}")
                except User.DoesNotExist:
                    logger.error(f"User not found: {data['user_id']}")
                    return Response({'error': 'Người dùng không tồn tại'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
            else:
                customer = Customer.objects.create(
                    name=data['customer_name'],
                    phone=data['customer_phone'],
                    email=data.get('customer_email', ''),
                    address=data.get('address', ''),
                    loyalty_point=0
                )
                logger.info(f"New guest customer created: {customer.customer_id}")

            # Tạo đơn hàng
            order = Order.objects.create(
                customer=customer,
                total_amount=float(data['total_amount']),
                discount=float(data.get('discount', 0)),
                final_amount=float(data['final_amount']),
                payment_method=data['payment_method']
            )
            logger.info(f"Order created: {order.order_id}")

            # Tạo chi tiết đơn hàng
            for item in data['items']:
                try:
                    product = Product.objects.get(pk=item['product_id'])
                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=int(item['quantity']),
                        unit_price=float(item['unit_price']),
                        sub_total=float(item['sub_total'])
                    )
                    logger.info(f"Added product {product.id} to order")
                except Product.DoesNotExist:
                    logger.error(f"Product not found: {item['product_id']}")
                    raise Exception(f"Sản phẩm ID {item['product_id']} không tồn tại")

            # Tính điểm tích lũy
            points_rate = 0.1 if (data.get('isLoggedIn') and data.get('user_id')) else 0.01
            points_earned = int(float(data['final_amount']) * points_rate)
            customer.loyalty_point += points_earned
            customer.save()
            logger.info(f"Added {points_earned} points to customer")

            response_data = {
                'success': True,
                'order_id': order.order_id,
                'customer_id': customer.customer_id,
                'loyalty_point': customer.loyalty_point,
                'points_earned': points_earned
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Order creation failed: {str(e)}", exc_info=True)
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Tạo đơn hàng thất bại. Vui lòng thử lại.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)