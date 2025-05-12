from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Category view
@api_view(['POST', 'GET'])
def category_list(request):
    if request.method == 'GET':
        queryset = Category.objects.annotate(
            product_count = Count('products')
        )
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    if request.method == 'GET':
        category = get_object_or_404(
            Category.objects.annotate(product_count=Count('products')), 
            pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        category = get_object_or_404(Category, pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'Unable to delete category that has product.'}, status=status.HTTP_409_CONFLICT)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# product view
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('category').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        product = get_object_or_404(Product, pk=pk)
        if product.order_items.count() > 0:
            return Response({'error': 'Unable to delete ordered product.'}, status=status.HTTP_409_CONFLICT)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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