from django.conf import settings
from django.core.cache import cache


def get_category_subjects(object_list):
    # При включенном ключе используем кэш, иначе бд
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        # Если в кэше нет объекта, получает и записывает
        if category_list is None:
            category_list = object_list
            cache.set(key, category_list)
    else:
        category_list = object_list
    return category_list