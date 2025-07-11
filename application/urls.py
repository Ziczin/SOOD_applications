from django.urls import path
from .views import dashboard, form_manager

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('form-manager/', form_manager, name="form-manager"),
]

