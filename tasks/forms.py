from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]
        widgets = {
            'due_date': DatePickerInput(format='%Y-%m-%d')
        }


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "All"),
        ("my", "My tasks"),
        ("todo", "To do"),
        ("in_progress", "In progress"),
        ("done", "Done"),
        ("overdue", "Overdue"),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='status', required=False)

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "media"]

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'media': forms.FileInput()
        }
