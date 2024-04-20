from django.urls import path
from tasks.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('user-cabinet/', UserCabinetView.as_view(), name='user-cabinet'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/complete/', TaskComplete.as_view(), name='task-complete'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/like/<int:pk>/', CommentLikeToggle.as_view(), name='comment-like-toggle'),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy('tasks:task-list')), name="logout"),
]

app_name = "tasks"