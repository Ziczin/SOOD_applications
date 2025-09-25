from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class Mixed(LoginRequiredMixin, TemplateView):
    template_name = 'application/builder.html'

class DashboardView(Mixed): extra_context = {'variant': 'dashboard'}
class FormManagerView(Mixed): extra_context = {'variant': 'form_manager'}
class DemoDashboardView(Mixed): extra_context = {'variant': 'dashboard'}
class DemoFormManagerView(Mixed): extra_context = {'variant': 'demo_form_manager'}
class EnumsManagerView(Mixed): extra_context = {'variant': 'enums_manager'}
class UsersManagerView(Mixed): extra_context = {'variant': 'users_manager'}
class FieldsManagerView(Mixed): extra_context = {'variant': 'fields_manager'}
