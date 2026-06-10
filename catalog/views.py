from django.shortcuts import render


def home(request):
    """Контроллер для главной страницы"""
    return render(request, 'catalog/home_page.html')


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