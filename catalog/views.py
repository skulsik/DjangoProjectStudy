from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from catalog.forms import *
from catalog.models import Product, Blog, Version
from django.views import generic

from catalog.modules.services.cache import get_category_subjects


class AllProductsView(generic.ListView):
    """ Все продукты """
    model = Product
    extra_context = {
        'title': 'Список последних товаров'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version = Version.objects.filter(publication=True)
        context_data['version_list'] = version
        context_data['user'] = self.request.user
        return context_data


class ProductView(generic.DetailView):
    """ Отображение одного продукта """
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    """ Создание продукта """
    model = Product
    permission_required = "catalog.add_product"
    form_class = ProductCreateViewForm

    def get_success_url(self):
        """ Берем slug из данного объекта """
        return reverse_lazy('catalog:product_view', args=(self.object.id,))

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.user = self.request.user
        # Сохраняет в бд
        self.object.save()
        return super(ProductCreateView, self).form_valid(form)


class UserToFormMixin(object):
    def get_form_kwargs(self):
        kwargs = super(UserToFormMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ProductUpdateView(UserToFormMixin, LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    """ Обновление продукта """
    model = Product
    permission_required = "catalog.change_product"
    form_class = ProductCreateViewForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:product_update', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        Versionformset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = Versionformset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = Versionformset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    """ Удаление продукта """
    model = Product
    permission_required = "catalog.delete_product"
    success_url = reverse_lazy('catalog:products')


class CategoryView(generic.ListView):
    """ Отображение одного продукта """
    model = Category

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['category_list'] = get_category_subjects(self.object_list)
        return context_data


class BlogsView(generic.ListView):
    """ Все блоги """
    model = Blog
    extra_context = {
        'title': 'Статьи'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication=True)
        return queryset


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    """ Создание блога """
    model = Blog
    form_class = BlogCreateViewForm

    def get_success_url(self):
        """ Берем slug из данного объекта """
        return reverse_lazy('catalog:blog_view', args=(self.object.slug,))


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    """ Обновление блога """
    model = Blog
    form_class = BlogCreateViewForm
    success_url = reverse_lazy('catalog:blogs')


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    """ Удаление блога """
    model = Blog
    success_url = reverse_lazy('catalog:blogs')


class BlogView(generic.DetailView):
    """ Отображение одного блога """
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
    """ Страница контакты """
    if request.method == 'POST':
        name: str = request.POST.get('name')
        phone: str = request.POST.get('phone')
        message: str = request.POST.get('message')
        print(f"Имя: {name}.\nТелефон: {phone}.\nСообщение: {message}.")
    return render(request, 'catalog/contacts.html')
