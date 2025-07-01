from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Form

@login_required
def dashboard(request):
    forms_list = list(Form.objects.all().values())
    print(forms_list)
    return render(request, 'application/dashboard.html', {'forms': forms_list}) 
