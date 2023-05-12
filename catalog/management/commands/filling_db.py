import json

from django.core.management import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from catalog.models import Product, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Получает все объекты таблиц БД
        product = Product.objects.all()
        category = Category.objects.all()

        # Удаляет все объекты таблиц БД
        product.delete()
        category.delete()

        # Сброс ключей
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Category, Product])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        # Читает json с резервом БД
        with open('data_my_app.json', 'r') as file:
            data_json = json.loads(file.read())

        product_objects = []
        category_objects = []

        # Заполнение объектами
        for item in data_json:
            if item['model'] == 'catalog.category':
                category_objects.append(Category(**item['fields']))
            if item['model'] == 'catalog.product':
                product_objects.append(Product(**item['fields']))

        # Запись объектов в БД
        Category.objects.bulk_create(category_objects)
        Product.objects.bulk_create(product_objects)
