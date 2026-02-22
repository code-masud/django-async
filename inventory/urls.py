from django.urls import path
from . import views


app_name = 'inventory'
urlpatterns = [
    path('inventory/', views.inventory_value, name='inventory_value'),
    path('product/', views.product_list, name='product_list'),
    path('category/', views.category_summery, name='category_summery'),
    path('movements/<int:pk>/', views.product_movements, name='product_movements'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
