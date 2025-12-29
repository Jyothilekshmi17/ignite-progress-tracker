from django import forms
from .models import Note, Topic, Project, Task, Milestone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows':6}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'status', 'summary', 'difficulty', 'resources']
        widgets = {'summary': forms.Textarea(attrs={'rows':3}), 'resources': forms.Textarea(attrs={'rows':3})}

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tech_stack', 'progress', 'demo_url', 'repo_url', 'deadline']
        widgets = {'description': forms.Textarea(attrs={'rows':4})}

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'status', 'due_date', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows':3})}

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'badge_url', 'date', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows':3})}

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]