from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.list_products),
    path('products/create/', views.create_product),
    path('products/<int:pk>/', views.get_product),
    path('products/<int:pk>/update/', views.update_product),
    path('products/<int:pk>/delete/', views.delete_product),
]