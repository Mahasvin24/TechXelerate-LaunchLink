from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ProjectRequest, Project, Task, VolunteerLog
from django.apps import apps
Business = apps.get_model('accounts', 'Business')
Client = apps.get_model('accounts', 'Client')
Volunteer = apps.get_model('accounts', 'Volunteer')
from django import forms
from django.contrib.auth.forms import UserCreationForm
import pprint


class VolunteerLogForm(forms.ModelForm):
    hours = forms.DecimalField(max_digits=3, decimal_places=1)
    description = forms.Textarea()
    class Meta:
        model = VolunteerLog
        fields = ['hours', 'description']
        
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project_id', None)
        super(VolunteerLogForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        volunteer_log = super(VolunteerLogForm, self).save(commit=False)
        volunteer_log.project = Project.objects.get(id=self.project)
        volunteer_log.save(commit)
        return volunteer_log
    
        
class ProjectRequestForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    description = forms.Textarea()
    is_business = forms.BooleanField(initial=False, required=False)
    business = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=False)
    
    class Meta:
        model = ProjectRequest
        fields = ['is_business', 'business', 'title', 'description']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProjectRequestForm, self).__init__(*args, **kwargs)
        if self.user is not None:
            self.fields['business'].queryset = Business.objects.filter(user=Client.objects.get(user=self.user)) 
            
    def save(self, commit=True):
        project = super(ProjectRequestForm, self).save(commit=False)
        project.client = Client.objects.get(user=self.user)
        project.business = self.cleaned_data['business']
        
        if commit:
            project.save()
    
        return project
    
    def is_valid(self) -> bool:
        # if self.cleaned_data['is_business'] and :
        #     return False
        return super().is_valid()
        

class ProjectForm(forms.ModelForm):

    managers = forms.ModelMultipleChoiceField(queryset=Volunteer.objects.all(), widget=forms.CheckboxSelectMultiple)
    developers = forms.ModelMultipleChoiceField(queryset=Volunteer.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Project
        fields = ['managers', 'developers']
    
    def __init__(self, *args, **kwargs):
        self.request_id = kwargs.pop('request_id', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
    
    def is_valid(self) -> bool:
        if self.request_id is None:
            return False
        return super().is_valid()
            
    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        project.project_request = ProjectRequest.objects.get(id=self.request_id)
        
        if commit:
            project.save()
            devs = self.cleaned_data['developers']
            for d in devs:
                project.developers.add((d))
            managers = self.cleaned_data['managers']
            for m in managers:
                project.managers.add((m))
            project.save()
            
        return project
    
class TaskForm(forms.ModelForm):
    
    assign = forms.ModelMultipleChoiceField(queryset=Volunteer.objects.all(), widget=forms.CheckboxSelectMultiple)
    task_name = forms.CharField(max_length=100)
    task_description = forms.Textarea()
    
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'assign']
    
    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id', None)
        super(TaskForm, self).__init__(*args, **kwargs)
    
    def is_valid(self) -> bool:
        if self.project_id is None:
            return False
        return super().is_valid()
            
    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        task.project = Project.objects.get(id=self.project_id)
        
        if commit:
            task.save()
        
        return task