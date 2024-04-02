from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from tasks.models import *
from tasks.forms import *
from django.urls import reverse_lazy


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")
