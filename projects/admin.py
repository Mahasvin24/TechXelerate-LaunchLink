from django.contrib import admin
from .models import Project, ProjectRequest, Task, VolunteerLog
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_request', 'slug', 'status', 'created', 'id')
    filter_horizontal = ('developers', 'managers')
    list_filter = ('status', 'created')
    
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'is_business', 'client', 'id')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'task_name', 'task_description', 'created', 'completed', 'id')
    filter_horizontal = ('assign',)
    list_filter = ('completed', 'created')

class VolunteerLogAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'hours', 'description', 'id')    

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRequest, ProjectRequestAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(VolunteerLog, VolunteerLogAdmin)
