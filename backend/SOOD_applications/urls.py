from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from reactest.views import YTVideoView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/forms/', include('forms.urls')),
    path('', RedirectView.as_view(url='/sood-applications/')),
    path('api/applications/', include('application.urls')),
    path('api/', YTVideoView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
