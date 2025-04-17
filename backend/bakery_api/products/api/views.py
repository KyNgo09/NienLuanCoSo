from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from products.models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import tempfile
import json
from django.conf import settings

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            try:
                queryset = queryset.filter(category__category_id=int(category_id))
            except (ValueError, TypeError):
                print(f"category_id không hợp lệ: {category_id}")
        return queryset
    
    def update(self, request, *args, **kwargs):
        """
        Tùy chỉnh phương thức update để hỗ trợ cập nhật từng phần và xử lý lỗi.
        """
        partial = kwargs.pop('partial', True)  # Cho phép cập nhật từng phần
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def get_credentials(self):
        token_path = os.path.join(settings.BASE_DIR, 'credentials', 'token.json')
        client_secret_path = os.path.join(settings.BASE_DIR, 'credentials', 'client_secret.json')
        scopes = ['https://www.googleapis.com/auth/drive.file']

        if os.path.exists(token_path):
            return Credentials.from_authorized_user_file(token_path, scopes)

        flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
        return creds

    def get_or_create_folder(self, drive_service, folder_name="BakeryManagement_ProductImages"):
        folder_id_path = os.path.join(settings.BASE_DIR, 'credentials', 'folder_id.json')
        
        if os.path.exists(folder_id_path):
            with open(folder_id_path, 'r') as f:
                folder_id = json.load(f).get('folder_id')
                try:
                    drive_service.files().get(fileId=folder_id, supportsAllDrives=True).execute()
                    print(f"Sử dụng thư mục hiện có với ID: {folder_id}")
                    return folder_id
                except:
                    print(f"Thư mục với ID {folder_id} không hợp lệ, tạo thư mục mới...")

        folder_id = getattr(settings, 'DRIVE_FOLDER_ID', None)
        if folder_id:
            try:
                drive_service.files().get(fileId=folder_id, supportsAllDrives=True).execute()
                print(f"Sử dụng thư mục từ settings.py với ID: {folder_id}")
                with open(folder_id_path, 'w') as f:
                    json.dump({'folder_id': folder_id}, f)
                return folder_id
            except:
                print(f"Thư mục với ID {folder_id} không tồn tại, tạo thư mục mới...")
        
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id', supportsAllDrives=True).execute()
        new_folder_id = folder.get('id')
        print(f"Tạo thư mục mới với ID: {new_folder_id}")
        
        with open(folder_id_path, 'w') as f:
            json.dump({'folder_id': new_folder_id}, f)
        
        return new_folder_id

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        try:
            product = self.get_object()
            image_file = request.FILES.get('image')
            
            if not image_file:
                return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

            creds = self.get_credentials()
            drive_service = build('drive', 'v3', credentials=creds)
            folder_id = self.get_or_create_folder(drive_service)

            temp_file = tempfile.NamedTemporaryFile(delete=False)
            try:
                for chunk in image_file.chunks():
                    temp_file.write(chunk)
                temp_file.close()
                temp_file_path = temp_file.name

                file_metadata = {
                    'name': f'product_{product.product_id}_{image_file.name}',
                    'parents': [folder_id]
                }
                
                media = MediaFileUpload(temp_file_path, mimetype=image_file.content_type)
                file = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id, webViewLink',
                    supportsAllDrives=True
                ).execute()
                
                file_id = file.get('id')
                image_url = f"https://drive.google.com/uc?export=view&id={file_id}"
                
                permission = {
                    'type': 'anyone',
                    'role': 'reader'
                }
                drive_service.permissions().create(
                    fileId=file_id,
                    body=permission,
                    supportsAllDrives=True
                ).execute()
                
                product_image = ProductImage.objects.create(
                    product=product,
                    imageurl=image_url
                )
                
                serializer = ProductImageSerializer(product_image)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            finally:
                try:
                    os.unlink(temp_file_path)
                except OSError as e:
                    print(f"Không thể xóa file tạm {temp_file_path}: {str(e)}")
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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