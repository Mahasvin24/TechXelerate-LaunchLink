from django.urls import path
from . import views

app_name = "projects"
urlpatterns = [
    path("new-project/<int:request_id>", views.new_project, name="new-project"),
    path("new-request", views.new_request, name="new-request"),
    path("new-task/<int:project_id>", views.new_task, name="new-task"),
    path("<int:project_id>", views.project_view, name="project-view"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("requests", views.requests, name="requests"),
    path("reject-request/<int:request_id>", views.reject_request, name="reject-request"),
    path("tasks", views.tasks, name="tasks"),
    path("complete-task/<int:task_id>", views.complete_task, name="complete-task"),
    path("hours", views.hours, name="hours"),
    path("no-access", views.no_access, name="no-access"),
]