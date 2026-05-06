from django.urls import path
from . import views

urlpatterns = [
    path('exchange/', views.exchange),
    path('transactions/', views.list_transactions),
]