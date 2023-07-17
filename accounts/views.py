from django.shortcuts import render
from .forms import ClientSignUpForm
from django.contrib.auth import login
import pprint

# Create your views here.
def new_client(request):
    if request.method == 'POST':
        pprint.pprint(request.POST)
        pprint.pprint(request.FILES)
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