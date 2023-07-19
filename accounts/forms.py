from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Client, Business
from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

class ClientSignUpForm(UserCreationForm):
    img = forms.ImageField(
            widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    username = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
        
    
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    address = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'img', 'password1', 'password2']
        
        
    def save(self, commit=True):
        user = super(ClientSignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        user.number = self.cleaned_data['phone_number']
        user.img = self.cleaned_data['img']
        user.is_client = True
        
        if commit:
            user.save()
        
        requester = Client.objects.create(
            user=user,
        )
        return requester
    
class BusinessSignUpForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    description = forms.CharField()
    address = forms.CharField(max_length=150)

    class Meta:
        model = Business
        fields = ['name', 'address', 'description']

    def save(self, commit=True):
        business = super(BusinessSignUpForm, self).save(commit=False)
        business.name = self.cleaned_data['name']
        business.description = self.cleaned_data['description']
        business.address = self.cleaned_data['address']
        
        if commit:
            business.save()
        return business
    
    def __init__ (self, *args, **kwargs):
        super(BusinessSignUpForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Name'
        })
        self.fields['address'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Address'
        })
        self.fields['description'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Business Description'
        })