from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .form_checker import form_checker

from .models import Form


@login_required
def get_forms_by_user_department(request):
    dept = request.user.department
    qs = Form.objects.filter(department=dept, available=True)
    data = list(qs.values("id", "form_name"))
    return JsonResponse({"forms": data})


@login_required
def form_creation(request):
    errors = []
    if request.method == "POST":
        form = request.POST
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    return render(
        request,
        "forms/form_builder.html",
        {"form": form_checker(form), "errors": errors},
    )
