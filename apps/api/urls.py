from django.urls import path
from apps.api.views.users import RegisterView, LoginView, LogoutView, ChangeRoleView
from apps.api.views.forms import FormListView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/change_role/', ChangeRoleView.as_view(), name='change-role'),
    path('forms/', FormListView.as_view(), name='form-list'),

]
