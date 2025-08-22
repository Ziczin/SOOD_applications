from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('forms/', include('apps.forms.urls')),
    path('applications/', include('apps.application.urls')),
    path('', RedirectView.as_view(url='/users/login/')),
    path('api/', include('apps.api.urls')),
]
