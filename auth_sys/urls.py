from django.urls import path
from django.contrib.auth.views import LoginView
from .views import RegisterView
from django.urls import reverse_lazy

app_name = 'auth'

urlpatterns = [
    path("login/", LoginView.as_view(template_name="auth_sys/login.html", extra_context={'next': reverse_lazy('tasks:task-list')}), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
]