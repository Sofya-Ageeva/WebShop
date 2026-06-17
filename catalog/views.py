from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

def home(request):
    """Контроллер для главной страницы"""
    products = Product.objects.all()
    return render(request, 'catalog/home_page.html', {'products': products})


def contacts(request):
    """Контроллер для страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Вывод в консоль (для отладки)
        print(f"\nПолучено сообщение от {name} ({email}): {message}\n")

        return render(request, 'catalog/contacts.html', {
            'success': True,
            'name': name
        })

    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    """Контроллер для страницы товара"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})
