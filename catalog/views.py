from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Product
from .forms import ProductForm

class HomeView(ListView):
    """Главная страница со списком товаров"""
    model = Product
    template_name = 'catalog/home_page.html'
    context_object_name = 'products'

class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"\nПолучено сообщение от {name} ({email}): {message}\n")
        return render(request, self.template_name, {'success': True, 'name': name})


class ProductDetailView(DetailView):
    """Страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Добавление товара"""
    login_url = 'users:login'
    redirect_field_name = 'next'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара"""
    login_url = 'users:login'
    redirect_field_name = 'next'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    success_url = reverse_lazy('catalog:home')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара"""
    login_url = 'users:login'
    redirect_field_name = 'next'
    model = Product
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:home')