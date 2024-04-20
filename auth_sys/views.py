from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from auth_sys.forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "auth_sys/register.html"
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        user = form.save()
    
        if user:
            login(self.request, user)
            if user.is_authenticated:
                return HttpResponseRedirect(self.success_url)
            else:
                return redirect("auth_sys:login")

        return super().form_valid(form)

