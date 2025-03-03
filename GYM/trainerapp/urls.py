from django.urls import path
from . import views
from .views import trainer_login_view, view_users, manage_workouts
from trainerapp.models import Trainer

urlpatterns = [
    path('', views.trainer_dashboard, name='trainer_dashboard'), 
    path('login/', trainer_login_view, name='trainer_login'),
    path('view-users/', view_users, name='view_users'),
    path("manage-workouts/", manage_workouts, name="manage_workouts"),

    path('dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('manage-workouts/', views.manage_workouts, name='manage_workouts'),
    path('track-progress/', views.track_progress, name='track_progress'),
    path('medical-history/', views.view_medical_history, name='view_medical_history'),
    path('health-tips/', views.health_tips, name='health_tips'),
    path('logout/', views.trainer_logout, name='trainer_logout'),
]
