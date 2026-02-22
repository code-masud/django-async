from django.http import JsonResponse
from django.db.models import Q
from .models import Supplier, Category, Product, StockMovement

async def product_list(request):
    search = request.GET.get('search', '')

    queryset = Product.objects.filter(is_active=True)

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)|
            Q(category__name__icontains=search)
        )
    
    products = [
        item async for item in queryset.values('id', 'name', 'price', 'stock', 'category__name', 'supplier__name')
    ]

    return JsonResponse(products, safe=False)