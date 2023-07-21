from django.db import models
from django.utils.text import slugify
# Create your models here.

class ProjectRequest(models.Model):
    PENDING = "1"
    VERIFIED = "2"
    REJECTED = "3"
    request_status = (
        (PENDING, 'Pending Verification'),
        (VERIFIED, 'Verified'),
        (REJECTED, 'Rejected'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_business = models.BooleanField(default=False)
    business = models.ForeignKey('accounts.Business', on_delete=models.CASCADE, null=True, related_name='requests', default=None, blank=True)
    client = models.ForeignKey('accounts.Client', on_delete=models.CASCADE, null=True, related_name='requests')
    slug = models.SlugField()
    status = models.CharField(max_length=100, choices=request_status, default=PENDING)
    
    def save(self, *args, **kwargs):
        self.slug = slugify("request-" + self.title)
        super(ProjectRequest, self).save(*args, **kwargs)
        self.slug = slugify(self.slug + "-" + str(self.id))
        super(ProjectRequest, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.slug
    
    
class Project(models.Model):
    FINDING_VOLUNTEERS = '1'
    WORKING = '2'
    FINAL_TOUCHES = '3'
    COMPLETED = '4'
    
    project_status = (
        (FINDING_VOLUNTEERS, 'Finding Volunteers'),
        (WORKING, 'Working'),
        (FINAL_TOUCHES, 'Final Touches'),
        (COMPLETED, 'Completed'),
    )
    
    project_request = models.ForeignKey(ProjectRequest, on_delete=models.CASCADE, null=True, related_name='project')
    status = models.CharField(max_length=100, choices=project_status, default=FINDING_VOLUNTEERS)
    managers = models.ManyToManyField('accounts.Volunteer', related_name='projects_managed')
    developers = models.ManyToManyField('accounts.Volunteer', related_name='projects_developed')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    product_link = models.URLField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify("project-" + self.project_request.title)
        super(Project, self).save(*args, **kwargs)
        self.slug = slugify(self.slug + "-" + str(self.id))
        super(Project, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.slug

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assign = models.ManyToManyField('accounts.Volunteer', related_name='tasks_assigned')
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['project', 'task_name']

    def __str__(self):
        return(self.task_name)

class VolunteerLog(models.Model):
    volunteer = models.ForeignKey('accounts.Volunteer', on_delete=models.CASCADE, related_name='logs')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE) 
    date = models.DateField(auto_now_add=True)
    hours = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()