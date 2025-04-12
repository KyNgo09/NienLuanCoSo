# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from customers.models import Customer
import hashlib

# account/views.py
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'message': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User.objects.get(email=email, password=hashed_password)
        
        try:
            customer = Customer.objects.get(user=user)
            customer_data = {
                'customer_id': customer.customer_id,
                'name': customer.name,
                'phone': customer.phone,
                'email': customer.email,
                'address': customer.address,
                'loyalty_point': customer.loyalty_point,
            }
        except Customer.DoesNotExist:
            customer_data = None
        
        return Response({
            'message': 'Đăng nhập thành công',
            'user': {
                'email': user.email,
                'username': user.username,
                'id': user.id,  # Thêm user_id
            },
            'customer': customer_data,
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        print(f"Đăng nhập thất bại: Không tìm thấy email={email}")
        return Response({
            'message': 'Email hoặc mật khẩu không hợp lệ'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def register_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    username = request.data.get('username')

    if not email or not password:
        return Response({
            'message': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({
            'message': 'Email đã tồn tại'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User.objects.create(
            email=email,
            password=hashed_password, 
            username=username
        )
        customer = Customer.objects.create(
            user=user,
            loyalty_point=0
        )
        return Response({
            'message': 'Tạo tài khoản thành công',
            'user': {
                'email': user.email,
                'username': user.username,
            },
            'customer': {
                'customer_id': customer.customer_id,
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Register error: {str(e)}")
        return Response({
            'message': 'Failed to create account'
        }, status=status.HTTP_400_BAD_REQUEST)