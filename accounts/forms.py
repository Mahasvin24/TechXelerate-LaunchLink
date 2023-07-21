from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Client, Business, Volunteer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

class ClientSignUpForm(UserCreationForm):
    img = forms.ImageField()
    first_name = forms.CharField(max_length=100,)
    last_name = forms.CharField(max_length=100,)
    email = forms.EmailField(max_length=150,)    
    phone_number = PhoneNumberField()
    address = forms.CharField(max_length=100, )


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
    def __init__ (self, *args, **kwargs):
        super(ClientSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
        self.fields['address'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123 Sesame Street'
        })
        self.fields['phone_number'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 123 456 7890'
        })
        self.fields['img'].widget = forms.FileInput(attrs={
            'class': 'form-control',
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        })

class VolunteerSignUpForm(UserCreationForm):
    img = forms.ImageField()
    first_name = forms.CharField(max_length=100,)
    last_name = forms.CharField(max_length=100,)
    email = forms.EmailField(max_length=150,)    
    phone_number = PhoneNumberField()
    address = forms.CharField(max_length=100, )
    grade = forms.DecimalField(max_digits=2, decimal_places=0)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'grade', 'email', 'phone_number', 'address', 'img', 'password1', 'password2']
        
        
    def save(self, commit=True):
        user = super(VolunteerSignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        user.number = self.cleaned_data['phone_number']
        user.img = self.cleaned_data['img']
        user.is_volunteer = True
        
        if commit:
            user.save()
        
        requester = Volunteer.objects.create(
            user=user,
            grade_level=self.cleaned_data['grade'],
        )
        return requester
    def __init__ (self, *args, **kwargs):
        super(VolunteerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
        self.fields['address'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123 Sesame Street'
        })
        self.fields['phone_number'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 123 456 7890'
        })
        self.fields['img'].widget = forms.FileInput(attrs={
            'class': 'form-control',
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        })   
        self.fields['grade'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '10'
        })

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
