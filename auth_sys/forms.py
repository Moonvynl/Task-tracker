from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["username", "tg", "password1", "password2", "avatar"]
        widgets = {
            "avatar": forms.FileInput()
        }