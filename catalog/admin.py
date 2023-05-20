from django.contrib import admin

from catalog.models import Product, Category, Blog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'publication', 'number_of_views')
    prepopulated_fields = {"slug": ("name",)}
