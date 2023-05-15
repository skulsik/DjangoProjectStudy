from django.shortcuts import render
from catalog.models import Product


def index(request):
    object_list = Product.objects.all()
    for item in object_list:
        item.description = item.description[:100]
    context = {
        'object_list': object_list
    }
    return render(request, 'catalog/index.html', context)


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    print(request.POST)
    if request.method == 'POST':
        name: str = request.POST.get('name')
        phone: str = request.POST.get('phone')
        message: str = request.POST.get('message')
        print(f"Имя: {name}.\nТелефон: {phone}.\nСообщение: {message}.")
    return render(request, 'catalog/contacts.html')
