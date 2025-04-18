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
    images = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'price', 'description', 'stock_quantity', 'category', 'images']

    def get_images(self, obj):
        request = self.context.get('request')
        images = ProductImage.objects.filter(product=obj)
        validated_images = []
        for image in images:
            file_id = image.imageurl.split('id=')[-1] if 'id=' in image.imageurl else None
            if file_id:
                proxy_url = f"{request.build_absolute_uri('/api/products/proxy-image/')}?file_id={file_id}"
                validated_images.append({'imageurl': proxy_url})
        return validated_images