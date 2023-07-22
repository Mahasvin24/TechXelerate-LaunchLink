from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from pprint import pprint
from django.contrib.auth.decorators import login_required
from .forms import ProjectRequestForm, ProjectForm, TaskForm, VolunteerLogForm
from django.apps import apps
Client = apps.get_model('accounts', 'Client')
Volunteer = apps.get_model('accounts', 'Volunteer')
from .models import ProjectRequest, Project, Task

# Create your views here.

def reject_request(request, request_id):
    if ProjectRequest.objects.filter(id=request_id).exists() and request.user.is_volunteer:
        project_request = ProjectRequest.objects.get(id=request_id)
        project_request.status = '3'
        project_request.save()
        return redirect('projects:requests')
def requests(request):
    return render(request, 'projects/requests.html', {
        'requests' : ProjectRequest.objects.exclude(status = '3'),
        'rejected' : ProjectRequest.objects.filter(status = '3'),
    })

def dashboard(request):
    return render(request, 'projects/project_dashboard.html', {
        'projects_in_progress' : Project.objects.exclude(status = '4'),
        'completed_projects' : Project.objects.filter(status = '4'),
    })

def project_view(request, project_id):
    if Project.objects.filter(id=project_id).exists():
        project = Project.objects.get(id=project_id)
        context = {
            'project' : project,
            'tasks' : Task.objects.filter(project=project_id),
        }
        if request.user.is_authenticated:
            if request.method == 'POST' and request.user.is_volunteer:
                if 'is_task' in request.POST:
                    form = TaskForm(request.POST, **{'project_id': project_id})
                    if form.is_valid():
                        task = form.save()
                        return redirect('projects:dashboard')
                    else:
                        if request.user.is_volunteer:
                            context['hour_form'] = VolunteerLogForm(**{'project_id': project_id, 'user': request.user})
                        if request.user.is_volunteer and Volunteer.objects.get(user=request.user).projects_managed.filter(id=project_id).exists():
                            context['task_form'] = TaskForm(**{'project_id': project_id})
                        return render(request, 'projects/project_view.html', context)
                else:
                    form = VolunteerLogForm(request.POST, **{'project_id': project_id, 'user': request.user})
                    if form.is_valid():
                        volunteer_log = form.save()
                        return redirect('projects:dashboard')
                    else:
                        if request.user.is_volunteer:
                            context['hour_form'] = VolunteerLogForm(**{'project_id': project_id, 'user': request.user})
                        if request.user.is_volunteer and Volunteer.objects.get(user=request.user).projects_managed.filter(id=project_id).exists():
                            context['task_form'] = TaskForm(**{'project_id': project_id})
                        return render(request, 'projects/project_view.html', context)
            else:
                if request.user.is_volunteer:
                    context['hour_form'] = VolunteerLogForm(**{'project_id': project_id, 'user': request.user})
                if request.user.is_volunteer and Volunteer.objects.get(user=request.user).projects_managed.filter(id=project_id).exists():
                    context['task_form'] = TaskForm(**{'project_id': project_id})
                return render(request, 'projects/project_view.html', context)
        else:
            return render(request, 'projects/project_view.html', context)
    else:
        return redirect('projects:dashboard')

@login_required
def new_project(request, request_id):
    if request.user.is_volunteer and ProjectRequest.objects.filter(id=request_id).exists():
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES, **{'request_id': request_id})
            context = {'form':form}
            if form.is_valid():
                project = form.save()
                created = True
                context = {'created' : created}
                return redirect('projects:dashboard')
            else:
                return render(request, 'projects/new_project.html', context)
        else:
            form = ProjectForm(**{'request_id': request_id})
            context = {
                'form' : form,
                'project_request' : ProjectRequest.objects.get(id=request_id),
            }
            return render(request, 'projects/new_project.html', context)
    else:
        return redirect('projects:dashboard')
    
@login_required
def new_request(request):
    if request.user.is_client:
        if request.method == 'POST':
            form = ProjectRequestForm(request.POST, request.FILES, **{'user': request.user})
            context = {'form':form}
            if form.is_valid():
                req = form.save()
                created = True
                context = {'created' : created}
                return redirect('projects:dashboard')
            else:
                return render(request, 'projects/new_request.html', context)
        else:
            form = ProjectRequestForm(**{'user': request.user})
            context = {
                'form' : form,
            }
            return render(request, 'projects/new_request.html', context)
    else:
        return redirect('about:home')
    
@login_required
def new_task(request, project_id):
    pprint(Project.objects.get(id=project_id).managers)
    if Project.objects.filter(id=project_id).exists() and Project.objects.get(id=project_id).managers.filter(user = request.user).exists():
        if request.method == 'POST':
            form = TaskForm(request.POST, request.FILES, **{'project_id': project_id})
            context = {'form':form}
            if form.is_valid():
                task = form.save()
                created = True
                context = {'created' : created}
                return render(request, 'projects/new_task.html', {
                    'created' : created
                })
            else:
                return render(request, 'projects/new_task.html', context)
        else:
            form = TaskForm(**{'project_id': project_id})
            context = {
                'form' : form,
            }
            return render(request, 'projects/new_task.html', context)
    else:
        return redirect('about:home')