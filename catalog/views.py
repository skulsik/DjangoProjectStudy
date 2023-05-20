from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from catalog.models import Product, Blog
from django.views import generic

from catalog.modules.services.utils import unique_slugify


class AllProductsView(generic.ListView):
    model = Product
    extra_context = {
        'title': 'Список последних товаров'
    }


class ProductView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class BlogsView(generic.ListView):
    model = Blog
    extra_context = {
        'title': 'Статьи'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication=True)
        return queryset


class BlogCreateView(generic.CreateView):
    model = Blog
    fields = ('name', 'content', 'image', 'date_of_creation')

    def get_success_url(self):
        """ Берем slug из данного объекта """
        return reverse_lazy('catalog:blog_view', args=(self.object.slug,))


class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ('name', 'content', 'image', 'date_of_creation')
    success_url = reverse_lazy('catalog:blogs')


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blogs')


class BlogView(generic.DetailView):
    model = Blog
    extra_context = {
        'title': 'Статья'
    }

    def get_object(self, queryset=None):
        """ Получает объект, увеличивает просмотры """
        object_blog = super().get_object()
        object_blog.number_of_views += 1
        object_blog.save()
        return object_blog


def contacts(request):
    print(request.POST)
    if request.method == 'POST':
        name: str = request.POST.get('name')
        phone: str = request.POST.get('phone')
        message: str = request.POST.get('message')
        print(f"Имя: {name}.\nТелефон: {phone}.\nСообщение: {message}.")
    return render(request, 'catalog/contacts.html')
