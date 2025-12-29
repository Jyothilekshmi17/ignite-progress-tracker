from django.db import models
from django.conf import settings

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True, help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def __str__(self):
        return self.title

class Topic(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('learning', 'Learning'),
        ('mastered', 'Mastered'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    summary = models.TextField(blank=True)
    difficulty = models.PositiveSmallIntegerField(default=1)
    resources = models.TextField(blank=True, help_text='One URL per line')

    def resource_list(self):
        return [r.strip() for r in self.resources.splitlines() if r.strip()]

    def __str__(self):
        return self.name

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=300, blank=True, help_text='Comma-separated')
    progress = models.PositiveSmallIntegerField(default=0)
    demo_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('backlog', 'Backlog'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='backlog')
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Milestone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    badge_url = models.URLField(blank=True)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title