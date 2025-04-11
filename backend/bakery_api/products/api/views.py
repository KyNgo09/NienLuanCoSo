from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from products.models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import os
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def upload_to_google_drive(file_path, file_name):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'credentials', 'client_secret.json')

    if not file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError({"images": f"Tệp {file_name} không phải là ảnh hợp lệ."})
    if not os.path.exists(file_path):
        raise ValidationError({"images": f"File tạm {file_path} không tồn tại."})

    creds = None
    token_path = '../../token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=5173)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            raise ValidationError({"images": f"Lỗi xác thực Google Drive: {str(e)}"})

    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': file_name, 'mimeType': 'image/jpeg'}
    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        return str(file.get('webViewLink'))  # Ép về chuỗi để chắc chắn
    except Exception as e:
        error_msg = str(e)
        print(f"Lỗi Google Drive khi upload {file_name}: {error_msg}")
        raise ValidationError({"images": f"Lỗi khi tải ảnh {file_name} lên Google Drive: {error_msg}"})
import logging
logger = logging.getLogger(__name__)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            if 'images' in data:
                del data['images']

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            product = serializer.save()

            images = request.FILES.getlist('images')
            if not images:
                raise ValidationError({"images": "Cần ít nhất một hình ảnh."})

            for image in images:
                temp_path = f'media/temp/{image.name}'
                logger.info(f"Xử lý ảnh: {image.name}")
                try:
                    os.makedirs('media/temp', exist_ok=True)
                    with open(temp_path, 'wb+') as temp_file:
                        for chunk in image.chunks():
                            temp_file.write(chunk)
                    if not os.path.exists(temp_path):
                        raise ValidationError({"images": f"File tạm {temp_path} không được tạo."})
                    logger.info(f"Tệp tạm {temp_path} đã được tạo.")
                    image_url = upload_to_google_drive(temp_path, image.name)
                    logger.info(f"Ảnh {image.name} đã được tải lên: {image_url}")
                    ProductImage.objects.create(product=product, imageurl=image_url)
                except Exception as e:
                    logger.error(f"Lỗi xử lý ảnh {image.name}: {str(e)}")
                    raise ValidationError({"images": f"Lỗi xử lý ảnh {image.name}: {str(e)}"})
                finally:
                    try:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                    except Exception as e:
                        print(f"Cảnh báo: Không thể xóa file tạm {temp_path}: {str(e)}")

            # Lấy lại product từ DB để đảm bảo không giữ trạng thái cũ
            product = Product.objects.get(product_id=product.product_id)
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Lỗi trong create: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def product_list_create(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def delete_category(request, category_id):
    if request.method == "DELETE":
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return JsonResponse({"message": "Danh mục đã được xóa"}, status=200)

    return JsonResponse({"error": "Phương thức không được hỗ trợ"}, status=405)

@api_view(['PUT'])
def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    serializer = CategorySerializer(category, data=request.data, partial=True)  # partial=True để cho phép cập nhật từng phần
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)