from rest_framework import serializers
from products.models import Product, Category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'  

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    # category = CategorySerializer()  # Hiển thị thông tin category

    class Meta:
        model = Product
        fields = '__all__'

    # def create(self, validated_data):
    #     category_data = validated_data.pop('category')
    #     category, _ = Category.objects.get_or_create(**category_data)
    #     product = Product.objects.create(category=category, **validated_data)
    #     return product