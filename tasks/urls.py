from django.contrib import admin
from django.urls import path
from tasks.views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/new/', TaskCreateView.as_view(), name='task_new'),
]
