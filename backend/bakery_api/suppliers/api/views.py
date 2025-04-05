from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from suppliers.models import Supplier, SupplyOrder, SupplyOrderDetail
from .serializers import SupplierSerializer, SupplyOrderDetailSerializer, SupplyOrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplyOrderViewSet(viewsets.ModelViewSet):
    queryset = SupplyOrder.objects.all()
    serializer_class = SupplyOrderSerializer

class SupplyOrderDetailViewSet(viewsets.ModelViewSet):
    queryset = SupplyOrderDetail.objects.all()
    serializer_class = SupplyOrderDetailSerializer

@api_view(['GET', 'POST'])
def supplier_list_create(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def delete_supplier(request, supplier_id):
    if request.method == "DELETE":
        supplier = get_object_or_404(Supplier, id=supplier_id)
        supplier.delete()
        return JsonResponse({"message": "Đơn vị đã được xóa"}, status=200)

    return JsonResponse({"error": "Phương thức không được hỗ trợ"}, status=405)