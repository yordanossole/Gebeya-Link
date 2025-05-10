from rest_framework import serializers
from .models import Category, Product



class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True
    )
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'write_only': True, 'read_only': False}
        }