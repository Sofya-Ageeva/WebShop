from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView(), name='home'),
    path('contacts/', views.ContactsView(), name='contacts'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/', views.ProductCreateView.as_view(), name='add_product'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
]