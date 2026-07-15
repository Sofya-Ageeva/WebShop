from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .services import get_products_by_category, get_category_by_id, get_product_by_id, clear_category_cache
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Product
from .forms import ProductForm

class HomeView(ListView):
    """Главная страница со списком товаров"""
    model = Product
    template_name = 'catalog/home_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Только опубликованные продукты"""
        return Product.objects.filter(is_published=True)


class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"\nПолучено сообщение от {name} ({email}): {message}\n")
        return render(request, self.template_name, {'success': True, 'name': name})

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    """Страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('pk')
        product = get_product_by_id(product_id)
        if product is None:
            from django.http import Http404
            raise Http404("Продукт не найден")
        product.views_count += 1
        product.save()
        return product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Добавление товара"""
    login_url = 'users:login'
    redirect_field_name = 'next'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Присвоение автора продукту"""
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        clear_category_cache(form.instance.category_id)
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара"""
    login_url = 'users:login'
    redirect_field_name = 'next'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        """Проверка на возможность редактирования карточки модератором или автором"""
        product = self.get_object()
        user = self.request.user

        if user == product.owner:
            return True
        if user.has_perm('catalog.can_unpublish_product'):
            return True
        return False

    def form_valid(self, form):
        response = super().form_valid(form)
        clear_category_cache(self.object.category_id)
        return response

    def handle_no_permission(self):
        """Отправка оповещения об отсутствии прав"""
        messages.error(self.request, 'У вас нет прав для редактирования текущей карточки.')
        return redirect('catalog:home')

class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    """Удаление товара"""
    login_url = 'users:login'
    redirect_field_name = 'next'
    model = Product
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        """Проверка прав на удаление карточки"""
        product = self.get_object()
        user = self.request.user

        if user == product.owner:
            return True
        if user.has_perm('catalog.can_unpublish_product'):
            return True
        return False

    def handle_no_permission(self):
        """Отправка оповещения об отсутствии прав на удаление"""
        messages.error(self.request, 'У вас нет прав на удаление карточки.')
        return redirect('catalog:home')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        category_id = product.category_id
        response = super().delete(request, *args, **kwargs)
        clear_category_cache(category_id)
        return response


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Отмена публикации продукта (только для модераторов)"""
    login_url = 'users:login'
    redirect_field_name = 'next'
    model = Product
    fields = []
    template_name = 'catalog/product_unpublish.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        """Только модератор может отменять публикацию"""
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для отмены публикации.')
        return redirect('catalog:home')

    def form_valid(self, form):
        """Отменяем публикацию продукта"""
        product = self.get_object()
        product.is_published = False
        product.save()
        messages.success(self.request, f'Публикация продукта "{product.name}" отменена.')
        return super().form_valid(form)

class CategoryProductsView(ListView):
    """Список продуктов в категории (с кешированием)"""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_category_by_id(category_id)
        return context
