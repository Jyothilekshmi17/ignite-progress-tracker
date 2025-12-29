# replace the existing tasks_view with this function
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task, Project
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views import generic
from .models import Note, Topic, Project, Task, Milestone
from .forms import NoteForm, TopicForm, ProjectForm, TaskForm, MilestoneForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracker:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    notes = Note.objects.filter(user=user).order_by('-updated_at')[:6]
    projects = Project.objects.filter(user=user).order_by('-created_at')
    tasks = Task.objects.filter(user=user)
    milestones = Milestone.objects.filter(user=user).order_by('-date')[:5]

    stats = {
        'notes': Note.objects.filter(user=user).count(),
        'projects': projects.count(),
        'tasks': tasks.count(),
        'done_tasks': tasks.filter(status='done').count(),
    }

    # Simple weekly activity (mock) - counts of tasks created per last 7 days
    today = timezone.now().date()
    week = []
    for i in range(6, -1, -1):
        day = today - timezone.timedelta(days=i)
        cnt = Task.objects.filter(user=user, created_at__date=day).count()
        week.append({'day': day.strftime('%a'), 'value': cnt})

    return render(request, 'tracker/dashboard.html', {'notes': notes, 'projects': projects, 'milestones': milestones, 'stats': stats, 'week': week})

# Generic CRUD with user restriction
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not getattr(obj, 'user', None):
            obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

# Notes
class NoteListView(LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = 'tracker/notes_list.html'
    context_object_name = 'notes'
    def get_queryset(self):
        qs = Note.objects.filter(user=self.request.user).order_by('-updated_at')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(content__icontains=q) | qs.filter(tags__icontains=q)
        return qs

class NoteCreateView(LoginRequiredMixin, OwnerMixin, generic.CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'tracker/note_form.html'
    success_url = reverse_lazy('tracker:notes_list')

class NoteUpdateView(LoginRequiredMixin, OwnerMixin, generic.UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'tracker/note_form.html'
    success_url = reverse_lazy('tracker:notes_list')

class NoteDeleteView(LoginRequiredMixin, OwnerMixin, generic.DeleteView):
    model = Note
    template_name = 'tracker/confirm_delete.html'
    success_url = reverse_lazy('tracker:notes_list')

# Topics
class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    template_name = 'tracker/topics_list.html'
    context_object_name = 'topics'
    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user).order_by('name')

class TopicCreateView(LoginRequiredMixin, OwnerMixin, generic.CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'tracker/topic_form.html'
    success_url = reverse_lazy('tracker:topics_list')

class TopicUpdateView(LoginRequiredMixin, OwnerMixin, generic.UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'tracker/topic_form.html'
    success_url = reverse_lazy('tracker:topics_list')

class TopicDeleteView(LoginRequiredMixin, OwnerMixin, generic.DeleteView):
    model = Topic
    template_name = 'tracker/confirm_delete.html'
    success_url = reverse_lazy('tracker:topics_list')

# Projects
class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'tracker/projects_list.html'
    context_object_name = 'projects'
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).order_by('-created_at')

class ProjectCreateView(LoginRequiredMixin, OwnerMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tracker/project_form.html'
    success_url = reverse_lazy('tracker:projects_list')

class ProjectUpdateView(LoginRequiredMixin, OwnerMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tracker/project_form.html'
    success_url = reverse_lazy('tracker:projects_list')

class ProjectDeleteView(LoginRequiredMixin, OwnerMixin, generic.DeleteView):
    model = Project
    template_name = 'tracker/confirm_delete.html'
    success_url = reverse_lazy('tracker:projects_list')

# Tasks (simple non-AJAX kanban)
@login_required
def tasks_view(request):
    user = request.user
    if request.method == 'POST':
        # create simple task or move
        action = request.POST.get('action')
        if action == 'create':
            form = TaskForm(request.POST)
            if form.is_valid():
                t = form.save(commit=False)
                t.user = user
                t.save()
                return redirect('tracker:tasks')
        elif action == 'move':
            tid = request.POST.get('task_id')
            status = request.POST.get('status')
            t = get_object_or_404(Task, pk=tid, user=user)
            t.status = status
            t.save()
            return redirect('tracker:tasks')
    tasks = Task.objects.filter(user=user).order_by('created_at')
    projects = Project.objects.filter(user=user)
    form = TaskForm()
    return render(request, 'tracker/tasks.html', {'tasks': tasks, 'form': form, 'projects': projects})

# Milestones
class MilestoneListView(LoginRequiredMixin, generic.ListView):
    model = Milestone
    template_name = 'tracker/milestones_list.html'
    context_object_name = 'milestones'
    def get_queryset(self):
        return Milestone.objects.filter(user=self.request.user).order_by('-date')

class MilestoneCreateView(LoginRequiredMixin, OwnerMixin, generic.CreateView):
    model = Milestone
    form_class = MilestoneForm
    template_name = 'tracker/milestone_form.html'
    success_url = reverse_lazy('tracker:milestones_list')

class MilestoneDeleteView(LoginRequiredMixin, OwnerMixin, generic.DeleteView):
    model = Milestone
    template_name = 'tracker/confirm_delete.html'
    success_url = reverse_lazy('tracker:milestones_list')

# Settings
@login_required
def settings_view(request):
    user = request.user
    message = ''
    if request.method == 'POST':
        theme = request.POST.get('theme')
        # store preference in session (simple) — could be persisted in DB later
        request.session['theme'] = theme
        message = 'Settings saved.'
    theme = request.session.get('theme', 'light')
    return render(request, 'tracker/settings.html', {'theme': theme, 'message': message})

# Export / Import
@login_required
def export_data(request):
    user = request.user
    data = {
        'notes': list(Note.objects.filter(user=user).values()),
        'topics': list(Topic.objects.filter(user=user).values()),
        'projects': list(Project.objects.filter(user=user).values()),
        'tasks': list(Task.objects.filter(user=user).values()),
        'milestones': list(Milestone.objects.filter(user=user).values()),
    }
    payload = json.dumps(data, default=str, indent=2)
    resp = HttpResponse(payload, content_type='application/json')
    resp['Content-Disposition'] = 'attachment; filename=ignite-backup.json'
    return resp

@login_required
def import_data(request):
    user = request.user
    if request.method == 'POST' and request.FILES.get('file'):
        f = request.FILES['file']
        try:
            data = json.load(f)
        except Exception as e:
            return render(request, 'tracker/import_result.html', {'error': str(e)})
        # Simple import: append objects for the user. This does NOT do deduplication.
        for n in data.get('notes', []):
            n.pop('id', None)
            Note.objects.create(user=user, **n)
        for t in data.get('topics', []):
            t.pop('id', None)
            Topic.objects.create(user=user, **t)
        for p in data.get('projects', []):
            p.pop('id', None)
            Project.objects.create(user=user, **p)
        for tk in data.get('tasks', []):
            tk.pop('id', None)
            # tasks referencing project id in another DB won't map; set project None
            tk.pop('project_id', None)
            Task.objects.create(user=user, **tk)
        for m in data.get('milestones', []):
            m.pop('id', None)
            Milestone.objects.create(user=user, **m)
        return render(request, 'tracker/import_result.html', {'ok': True})
    return render(request, 'tracker/import.html')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracker:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def tasks_view(request):
    user = request.user
    # status tuples for template (label, key)
    statuses = [('Backlog', 'backlog'), ('In Progress', 'in_progress'), ('Done', 'done')]

    if request.method == 'POST':
        # create simple task or move
        action = request.POST.get('action')
        if action == 'create':
            form = TaskForm(request.POST)
            if form.is_valid():
                t = form.save(commit=False)
                t.user = user
                t.save()
                return redirect('tracker:tasks')
        elif action == 'move':
            tid = request.POST.get('task_id')
            status = request.POST.get('status')
            t = get_object_or_404(Task, pk=tid, user=user)
            t.status = status
            t.save()
            return redirect('tracker:tasks')

    tasks = Task.objects.filter(user=user).order_by('created_at')
    projects = Project.objects.filter(user=user)
    form = TaskForm()
    return render(request, 'tracker/tasks.html', {
        'tasks': tasks,
        'form': form,
        'projects': projects,
        'statuses': statuses,  # <-- pass statuses to template
    })