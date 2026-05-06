from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.list_users),
    path('users/create/', views.create_user),
    path('users/<int:pk>/', views.get_user),
    path('users/<int:pk>/deposit/', views.add_points),
]