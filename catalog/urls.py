from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import *

app_name = CatalogConfig.name

urlpatterns = [
    path('', AllProductsView.as_view(), name='products'),
    path('product/<int:pk>', ProductView.as_view(), name='product_view'),
    path('product/create_product', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('contacts', contacts, name='contacts'),
    path('blogs', BlogsView.as_view(), name='blogs'),
    path('blog/create_blog', BlogCreateView.as_view(), name='create_blog'),
    path('blog/update/<slug:slug>', BlogUpdateView.as_view(), name='update_blog'),
    path('blog/delete/<slug:slug>', BlogDeleteView.as_view(), name='delete_blog'),
    path('blog/<slug:slug>', BlogView.as_view(), name='blog_view')
]
