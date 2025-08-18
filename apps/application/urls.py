from django.urls import path
from .views import dashboard, form_manager, demo_1, demo_2, demo_3, demo_dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('form-manager/', form_manager, name="form-manager"),
    path('demo-1/', demo_1, name="demo-1"),
    path('demo-2/', demo_2, name="demo-2"),
    path('demo-3/', demo_3, name="demo-3"),
    path('demo-dashboard/', demo_dashboard, name="demo-dashboard"),
]

