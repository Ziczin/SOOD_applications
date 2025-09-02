from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'application/builder.html'
    extra_context = {'variant': 'dashboard'}

class FormManagerView(LoginRequiredMixin, TemplateView):
    template_name = 'application/builder.html'
    extra_context = {'variant': 'form_manager'}

class DemoDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'application/builder.html'
    extra_context = {'variant': 'dashboard'}

class DemoFormManagerView(LoginRequiredMixin, TemplateView):
    template_name = 'application/builder.html'
    extra_context = {'variant': 'demo_form_manager'}
