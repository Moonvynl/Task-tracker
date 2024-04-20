from calendar import c
from django.db import models
from django.db import models
from django.urls import reverse
from django.conf import settings




class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To do"),
        ("in_progress", "In progress"),
        ("done", "Done")
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ]

    title = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=31, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=31, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateTimeField(blank=True, null=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")

    def get_absolute_url(self):
        return reverse('tasks:task-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Task"


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to="comment_media/", blank=True, null=True)

    def get_absolute_url(self):
        return self.task.get_absolute_url()

    class Meta:
        verbose_name = "Comment"
        ordering = ["-created_at"]


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')