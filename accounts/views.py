from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ClientSignUpForm, BusinessSignUpForm
from .models import Client, Business, User, Volunteer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
import pprint
from django.contrib.auth.decorators import login_required


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
                return render(request, 'accounts/new_business.html', {
                    'created' : created
                })
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
            return render(request, 'accounts/login.html', {'login_form':form})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('about:home'))