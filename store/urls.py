from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list),
    path('categories/<int:pk>', views.category_detail, name='category-detail'),
    path('products/', views.product_list),
    path('products/<int:pk>', views.product_detail),
]

# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:id>', views.ProductDetail.as_view()),
#     path('categories/', views.CategoryList.as_view()),
#     path('categories/<int:pk>', views.CategoryDetail.as_view(), name='category-detail'),
# ]