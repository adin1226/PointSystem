from django.urls import path
from . import views
from .views import RegisterView, CustomTokenView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # page
    path('product-list', views.product_list),
    path('login-page/', views.login_page), 
    path('register-page/', views.register_page),
    # 讓JS去call的API
    path('register/', RegisterView.as_view()),
    path('login/', CustomTokenView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    path('users/', views.list_users),
    # path('users/create/', views.create_user),
    path('users/<int:pk>/', views.get_user), # 取得指定ID使用者資訊
    path('users/now/', views.get_now_user), # 取得現在登入的使用者資訊
    path('users/deposit/', views.add_points),
]