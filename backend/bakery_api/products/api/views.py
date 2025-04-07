from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from products.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        # Tạo sản phẩm trước
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # Xử lý hình ảnh nếu có
        images = request.FILES.getlist('images')  # Giả sử gửi nhiều ảnh qua field 'images'
        for image in images:
            # Lưu tạm ảnh vào server
            temp_path = f'media/temp/{image.name}'
            with open(temp_path, 'wb+') as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
            
            # Tải lên Google Drive và lấy URL
            image_url = upload_to_google_drive(temp_path, image.name)
            
            # Lưu URL vào DB
            ProductImage.objects.create(product=product, image=image_url)
            
            # Xóa file tạm
            os.remove(temp_path)

        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        # Cập nhật sản phẩm
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # Xử lý thêm ảnh mới nếu có
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                temp_path = f'media/temp/{image.name}'
                with open(temp_path, 'wb+') as temp_file:
                    for chunk in image.chunks():
                        temp_file.write(chunk)
                image_url = upload_to_google_drive(temp_path, image.name)
                ProductImage.objects.create(product=product, image=image_url)
                os.remove(temp_path)

        return Response(serializer.data)

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

@csrf_exempt
def delete_category(request, category_id):
    if request.method == "DELETE":
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return JsonResponse({"message": "Danh mục đã được xóa"}, status=200)

    return JsonResponse({"error": "Phương thức không được hỗ trợ"}, status=405)