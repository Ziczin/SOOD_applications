from django.urls import path
from .views import register, login_view, logout_view
from .views import admin_dashboard, kitchen_dashboard, user_dashboard

urlpatterns = [
    path('menu/', register, name='register'),
    path('create-order/', login_view, name='login'),
    path('orders/', logout_view, name='logout'),
]

