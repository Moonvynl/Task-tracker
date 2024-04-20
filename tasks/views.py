from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView, View
from tasks.models import *
from tasks.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from tasks.mixins import *
from django.core.exceptions import ValidationError
from datetime import datetime

class UserCabinetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_cabinet.html')


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        if status:
            if status == 'my':
                if self.request.user.is_authenticated:
                    queryset = queryset.filter(creator = self.request.user)
            elif status == 'overdue':
                current_time = datetime.now()
                queryset = queryset.filter(due_date__lt = current_time)
                print(current_time, queryset)
            else:
                queryset = queryset.filter(status = status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskCommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = TaskCommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.creator = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('tasks:task-detail', pk = comment.task.pk)
        else:
            raise ValidationError("Form is not valid")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "tasks/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin ,DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskComplete(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, pk = task_id)
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))


class CommentUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Comment
    fields = ['content']
    
    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs = {"pk": self.object.task.id})

    def form_valid(self, form):
        comment = self.get_object()
        if comment.creator == self.request.user:
            return super().form_valid(form)
        else:
            raise PermissionDenied("You don't have permissions")


class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    
    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs = {"pk": self.object.task.id})


class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        like_qs = Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            Like.objects.create(comment=comment, user=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())

