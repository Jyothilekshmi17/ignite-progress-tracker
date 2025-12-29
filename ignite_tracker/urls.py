from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password
    path('accounts/register/', views.register, name='register'),  # <-- ensure 'register' is spelled correctly
    path('', include('tracker.urls')),
]