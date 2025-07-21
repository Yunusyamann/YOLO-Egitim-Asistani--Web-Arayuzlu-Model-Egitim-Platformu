from django.urls import path
from . import views

app_name = 'trainer'

urlpatterns = [
    path('', views.training_view, name='training_view'),
    path('job/<int:job_id>/', views.job_status_view, name='job_status'),
    path('jobs/', views.list_jobs_view, name='list_jobs'),
]