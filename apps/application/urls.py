from django.urls import path
from .views import dashboard, form_manager, demo_form_manager

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('form-manager/', form_manager, name="form-manager"),
    path('demo-form-manager/', demo_form_manager, name="demo-form-manager"),
]

