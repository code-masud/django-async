from celery import shared_task
from django.core.cache import cache
from .models import Product
import time
import random

CACHE_KEY = "product_list_v3"
TTL = 300

@shared_task(bind=True, max_retries=3)
def rebuild_product_cache(self):
    try:
        queryset = (
            Product.objects
            .select_related("category", "supplier")
            .values(
                "id",
                "name",
                "price",
                "stock",
                "category__name",
                "supplier__name",
            )
        )

        data = list(queryset)

        payload = {
            "data": data,
            "expires_at": time.time() + TTL
        }

        # Add jitter to avoid synchronized expiration
        jitter = random.randint(0, 60)

        cache.set(CACHE_KEY, payload, TTL + jitter)

    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)