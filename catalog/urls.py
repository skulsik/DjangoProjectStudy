from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import *

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('contacts', contacts, name='contacts')
]
