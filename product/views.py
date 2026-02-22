import asyncio
from django.shortcuts import render
from django.http import JsonResponse
from .models import Item


async def product_list(request):
    data = [
        item async for item in Item.objects.values("id", "name", "sku", "price", "category__name")
    ]
    # data = list(Item.objects.values('id', 'name', 'sku', 'price'))
    return JsonResponse(data, safe=False)