from rest_framework import serializers
from products.models import Product, Category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['imageurl']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(source='productimage_set', many=True)
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'price', 'description', 'category', 'images']

   