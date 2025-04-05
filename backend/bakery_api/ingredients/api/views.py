from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from ingredients.models import Unit, Ingredient
from .serializers import UnitSerializer, IngredientSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

# ==== ĐƠN VỊ ===
@api_view(['GET', 'POST'])
def unit_list_create(request):
    if request.method == 'GET':
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def delete_unit(request, unit_id):
    if request.method == "DELETE":
        unit = get_object_or_404(Unit, id=unit_id)
        unit.delete()
        return JsonResponse({"message": "Đơn vị đã được xóa"}, status=200)

    return JsonResponse({"error": "Phương thức không được hỗ trợ"}, status=405)

#=== NGUYÊN LIỆU ====
@api_view(['GET', 'POST'])
def ingredient_list_create(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def delete_ingredient(request, ingredient_id):
    if request.method == "DELETE":
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        ingredient.delete()
        return JsonResponse({"message": "Đơn vị đã được xóa"}, status=200)

    return JsonResponse({"error": "Phương thức không được hỗ trợ"}, status=405)

