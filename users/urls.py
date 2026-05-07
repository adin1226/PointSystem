from django.urls import path
from . import views
from .views import RegisterView, CustomTokenView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('product-list', views.product_list),
    # page
    path('login-page/', views.login_page), 
    path('register-page/', views.register_page),
    # 讓JS去call的API
    path('register/', RegisterView.as_view()),
    path('login/', CustomTokenView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),


    path('users/', views.list_users),
    path('users/create/', views.create_user),
    path('users/<int:pk>/', views.get_user),
    path('users/deposit/', views.add_points),
]