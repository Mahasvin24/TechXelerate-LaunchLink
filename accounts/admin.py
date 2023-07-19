from django.contrib import admin
from .models import User, Client, Volunteer, Business
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'number', 'address', 'id')
    
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level' , 'volunteer_hours', 'id')
    
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'address', 'id')
    
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Business, BusinessAdmin)