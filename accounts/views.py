from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ClientSignUpForm, BusinessSignUpForm, VolunteerSignUpForm
from .models import Client, Business, User, Volunteer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
import pprint
from django.contrib.auth.decorators import login_required
from django.apps import apps
ProjectRequest = apps.get_model('projects', 'ProjectRequest')

def business_profile(request, business_id):
    if Business.objects.filter(id=business_id).exists():
        business = Business.objects.get(id=business_id)
        tmp = [ project.project.all() for project in business.requests.all()]

        projects = []
        for t in tmp:
            for p in t:
                projects.append(p)
        context = {
            'business' : business,
            'projects' : projects,
        }
        return render(request, 'accounts/business_profile.html', context)
    else:
        return redirect('about:home')
    

def client_profile(request, client_id):
    if Client.objects.filter(id=client_id).exists():
        client = Client.objects.get(id=client_id)
        context = {
            'client' : client,
            'request_rejected' : ProjectRequest.objects.filter(client=client, status=3),
            'request_accepted' : ProjectRequest.objects.filter(client=client).exclude(status=3),
        }
        return render(request, 'accounts/client_profile.html', context)
    else:
        return redirect('about:home')

def volunteer_profile(request, volunteer_id):
    if Volunteer.objects.filter(id=volunteer_id).exists():
        volunteer = Volunteer.objects.get(id=volunteer_id)
        context = {
            'volunteer' : volunteer,
            'tasks' : volunteer.tasks_assigned.all(),
        }
        return render(request, 'accounts/volunteer_profile.html', context)
    else:
        return redirect('projects:dashboard')
    


# Create your views here.
def new_client(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST, request.FILES)
        context = {'form':form}
        if form.is_valid():
            client = form.save()
            created = True
            login(request, client.user)
            context = {'created' : created}
            return render(request, 'accounts/new_client.html', {
                'created' : created
            })
        else:
            return render(request, 'accounts/new_client.html', context)
    else:
        form = ClientSignUpForm()
        context = {
            'form' : form,
        }
        return render(request, 'accounts/new_client.html', context)

def new_volunteer(request):
    if request.method == 'POST':
        form = VolunteerSignUpForm(request.POST, request.FILES)
        context = {'form':form}
        if form.is_valid():
            volunteer = form.save()
            created = True
            login(request, volunteer.user)
            context = {'created' : created}
            return redirect('projects:dashboard')
        else:
            return render(request, 'accounts/new_volunteer.html', context)
    else:
        form = VolunteerSignUpForm()
        context = {
            'form' : form,
        }
        return render(request, 'accounts/new_volunteer.html', context)

@login_required
def new_business(request):
    # Check for auth
    if request.user.is_client:
        if request.method == 'POST':
            form = BusinessSignUpForm(request.POST, request.FILES)
            # form.user = Client.objects.get(user=request.user)
            context = {'form':form}
            if form.is_valid():
                business = form.save(commit=False)
                business.user = Client.objects.get(user=request.user)
                business.save()
                created = True
                context = {'created' : created}
                return redirect('projects:dashboard')
            else:
                return render(request, 'accounts/new_business.html', context)
        else:
            form = BusinessSignUpForm()
            context = {
                'form' : form,
            }
            return render(request, 'accounts/new_business.html', {
                'form' : form
            })
    else:
        return redirect('about:home')
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return redirect('about:home')
        else:
            return render(request, 'accounts/login.html', {'form':form})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('about:home'))