from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from pprint import pprint
from django.contrib.auth.decorators import login_required
from .forms import ProjectRequestForm, ProjectForm, TaskForm
from django.apps import apps
Client = apps.get_model('accounts', 'Client')
from .models import ProjectRequest, Project, Task

# Create your views here.
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
                return render(request, 'projects/new_project.html', {
                    'created' : created
                })
            else:
                return render(request, 'projects/new_project.html', context)
        else:
            form = ProjectForm(**{'request_id': request_id})
            context = {
                'form' : form,
            }
            return render(request, 'projects/new_project.html', context)
    else:
        return redirect('about:home')
    
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
                return render(request, 'projects/new_request.html', {
                    'created' : created
                })
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