from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from multiselectfield import MultiSelectField
from django.db import models
from django.conf import settings
import uuid

# Create your models here.

class User_task(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

prior_choices = (
    ('heigh', 'heigh'),
    ('medium', 'medium'),
    ('low', 'low'),
)

class Project(models.Model):
    IDproject = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    startDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, related_name='createdby') 
    description = models.TextField(blank=True)
    prior = models.CharField(max_length=50, choices=prior_choices, default='medium')
    participants = models.ForeignKey(Group,on_delete=models.CASCADE,
                                     related_name='participants',null=True, blank=True)

    def __str__(self):
        return self.IDproject

    def get_absolute_url(self):
        return reverse("detail_pro", kwargs={"pk": self.pk})

status_choices = (
    ('New', 'New'),
    ('Processing','Processing'),
    ('Finish','Finish'),
    ('Reject','Reject')
)

class Task(models.Model):
    ID_task = models.CharField(max_length=100,default='',unique=True)
    name_task = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,)
    note = models.TextField(blank=True)
    startDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    responsible_person = models.CharField(max_length=100,blank=True)
    supervisor = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=status_choices, default='New', blank=True)
    muc_do_hoan_thanh = models.IntegerField(default=0)
    document = models.FileField(upload_to='documents/',null=True, blank=True,)
    def __str__(self):
        return self.name_task
    
    def get_responsible_person(self):  
        return ",".join([str(p) for p in self.responsible_person.all()])

    def get_absolute_url(self):
        return reverse("task_edit", kwargs={"pk": self.pk})
