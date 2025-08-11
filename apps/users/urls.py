from django.urls import path
from .views import register, login_view, logout_view, sandbox
from .views import change_role

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-role/', change_role, name='change-role'),
    path('sandbox/', sandbox, name='sandbox'),
]

