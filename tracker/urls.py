from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Notes
    path('notes/', views.NoteListView.as_view(), name='notes_list'),
    path('notes/new/', views.NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),

    # Topics
    path('topics/', views.TopicListView.as_view(), name='topics_list'),
    path('topics/new/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic_edit'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='projects_list'),
    path('projects/new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # Tasks
    path('tasks/', views.tasks_view, name='tasks'),

    # Milestones
    path('milestones/', views.MilestoneListView.as_view(), name='milestones_list'),
    path('milestones/new/', views.MilestoneCreateView.as_view(), name='milestone_create'),
    path('milestones/<int:pk>/delete/', views.MilestoneDeleteView.as_view(), name='milestone_delete'),

    # Settings / Export Import
    path('settings/', views.settings_view, name='settings'),
    path('export/', views.export_data, name='export'),
    path('import/', views.import_data, name='import'),

]