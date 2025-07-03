from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Form
from users.models import CustomUser

@login_required
def dashboard(request):
    forms_list = list(Form.objects.all().values())
    user_data = CustomUser.objects.get(username=request.user)
    return render(
        request, 'application/dashboard.html',
        {'forms': forms_list, 'user': user_data}
    ) 
