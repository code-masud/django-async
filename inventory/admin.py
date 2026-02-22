from django.contrib import admin
from .models import Supplier, Category, Product, StockMovement


admin.site.register([Supplier, Category, Product, StockMovement])