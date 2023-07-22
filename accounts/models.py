from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum
class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254)
    number = PhoneNumberField(blank=True)
    img = models.ImageField(upload_to='avatars', default='avatars/blank_profile.png')
    address = models.CharField(max_length=150)
    is_volunteer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer')
    grade_level = models.IntegerField()
    # volunteer_hours = models.IntegerField(default = 0)
    # skills = models.TextField()
    # interests = models.TextField()
    # availability = models.TextField()  

    def __str__(self):
        return self.user.username
    
    def get_hours(self):
        return self.logs.aggregate(total_hours=Sum('hours')).get('total_hours') or 0
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='requester')
    
    def __str__(self):
        return self.user.username
    
class Business(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='businesses') 
    name = models.CharField(max_length=150)
    description = models.TextField()
    address = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name