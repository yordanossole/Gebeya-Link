from django.shortcuts import get_object_or_404

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('category').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):        
        product = get_object_or_404(Product, id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is ordered item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryList(APIView):
    def get(self, request):
        return

    def post(self, request):
        return

class CategoryDetail(APIView):
    def get(self, request, id):
        return
    
    def put(self, request, id):
        return
    
    def delete(self, request, id):
        return