from .models import Product, Category
from django.core.cache import cache
from django.shortcuts import get_object_or_404


def get_products_by_category(category_id):
    """Сервисная функция для получения продуктов по категории с кешированием."""
    cache_key = f'category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        print(f"Кеш для категории {category_id} не найден, загружаем из базы...")
        products = Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('category')

        # Сохраняем в кеш на 30 минут (1800 секунд)
        cache.set(cache_key, products, timeout=1800)
        print(f"Данные категории {category_id} сохранены в кеш на 30 минут")
    else:
        print(f"Данные категории {category_id} загружены из кеша")

    return products



def get_category_by_id(category_id):
    """Получение категории по ID"""
    return get_object_or_404(Category, pk=category_id)


def clear_category_cache(category_id):
    """Очистка кеша категории"""
    cache_key = f'category_{category_id}'
    cache.delete(cache_key)
    print(f"Кеш категории {category_id} очищен")


def get_product_by_id(product_id):
    """Сервисная функция для получения одного продукта с кешированием"""
    cache_key = f'product_{product_id}'
    product = cache.get(cache_key)

    if product is None:
        print(f"Кеш для продукта {product_id} не найден, загружаем из БД...")
        try:
            product = Product.objects.select_related('category').get(
                pk=product_id,
                is_published=True
            )
            cache.set(cache_key, product, timeout=900)  # 15 минут
            print(f"Продукт {product_id} сохранён в кеш на 15 минут")
        except Product.DoesNotExist:
            return None
    else:
        print(f"Продукт {product_id} загружен из кеша")

    return product