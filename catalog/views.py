from django.shortcuts import render


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
