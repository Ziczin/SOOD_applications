from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import form_create_form_data

from .form_builder import form_builder

form_create_form = form_builder(form_create_form_data)

@login_required
def form_creation(request):
    errors = []
    if request.method == 'POST':
        form = form_create_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = form_create_form()
    return render(request, 'forms/form_builder.html', {'form': form, 'errors': errors})

@login_required
def field_type_creation(request):
    pass

@login_required
def enum_tag_creation(request):
    pass

@login_required
def enum_elem_creation(request):
    pass

@login_required
def field_creation(request):
    pass


