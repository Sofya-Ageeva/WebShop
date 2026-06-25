from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            try:
                send_mail(
                    subject='Добро пожаловать в WebShop!',
                    message=f'Приветствуем вас, {user.email}!\n\n'
                            f'Вы успешно зарегистрировались в нашем магазине.\n'
                            f'Теперь вы можете просматривать товары и редактировать их.\n\n'
                            f'С уважением,\nКоманда WebShop',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f'Ошибка отправки письма: {e}')
                messages.warning(request, 'Аккаунт создан, но письмо не отправлено.')

            messages.success(request, f'Аккаунт {user.email} успешно создан!')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Авторизация пользователя"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.email}!')
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, 'Неверный email или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('catalog:home')

@login_required
def profile(request):
    """Страница профиля пользователя"""
    return render(request, 'users/profile.html', {'user': request.user})