from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q, Count, Sum, F, OuterRef, Subquery
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

async def product_detail(request, pk):
    product = await Product.objects.select_related(
        'category', 'supplier'
    ).aget(pk=pk)

    data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock,
        'category': product.category.name,
        'supplier': product.supplier.name,
    }

    return JsonResponse(data, safe=False)

async def category_summery(request):
    data = [
        item async for item in Category.objects.values('name').annotate(total_product=Count('product'))
    ]

    return JsonResponse(data, safe=False)

async def inventory_value(request):
    total = await Product.objects.aaggregate(
        total_value=Sum(F("price") * F("stock"))
    )

    return JsonResponse(total)

async def product_movements(request, pk):
    product = await Product.objects.prefetch_related(
        'movements'
    ).aget(pk=pk)

    movements = [
        {'qty': m.quantity, 'status': m.status} for m in product.movements.all()
    ]

    return JsonResponse({
        'product': product.name,
        'stock': product.stock,
        'movements': movements
    })

async def update_stock(request, pk):
    quantity = int(request.POST.get('quantity'))

    async with transaction.atomic():
        await Product.objects.filter(pk=pk).aupdate(
            stock=F('stock') + quantity
        )
    
    return JsonResponse({'status': 'updated'})

latest_movement = StockMovement.objects.filter(
    product=OuterRef("pk")
).order_by("-created_at")

async def product_latest_movement(request):

    queryset = Product.objects.annotate(
        last_quantity=Subquery(
            latest_movement.values("quantity")[:1]
        )
    )

    data = [
        item async for item in queryset.values(
            "name", "last_quantity"
        )
    ]

    return JsonResponse(data, safe=False)