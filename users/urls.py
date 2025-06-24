from django.urls import path
from .views import register, login_view, logout_view
from .views import kitchen_dashboard, user_dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('manager/', kitchen_dashboard, name='kitchen_dashboard'),
    path('user/', user_dashboard, name='user_dashboard'),
]

