# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
import hashlib

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
        
        return Response({
            'message': 'Đăng nhập thành công',
            'email': user.email,
            'username': user.username,
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
        return Response({
            'message': 'Tạo tài khoản thành công',
            'email': user.email,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Register error: {str(e)}")
        return Response({
            'message': 'Failed to create account'
        }, status=status.HTTP_400_BAD_REQUEST)