from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/', views.ProductCreateView.as_view(), name='add_product'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
path('unpublish/<int:pk>/', views.ProductUnpublishView.as_view(), name='unpublish_product'),
    path('category/<int:category_id>/', views.CategoryProductsView.as_view(), name='category_products'),

]