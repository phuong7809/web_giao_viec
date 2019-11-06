from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from .models import Project,Task
from .fields import GroupedModelChoiceField
from django.forms import ModelChoiceField

from django import forms

# team = list(Team.objects.all())
# CHOICES=[]
# for i in team:
#     CHOICES.append([i,i])

class ProjectForm(ModelForm):
    participants = forms.ModelChoiceField(queryset=Group.objects.all())
    # participants = GroupedModelChoiceField(
    #     queryset=Team.objects.exclude(group=None),
    #     choices_groupby='group')
    # IDproject = forms.CharField(label='Ma_DA')
    class Meta:
        model = Project
        fields = ('name', 'startDate',
                  'endDate', 'description', 'prior', 'participants')

users=list(User.objects.all())
OPTIONS = []
for i in users:
    OPTIONS.append([i,i]) 
# 

class TaskForm(ModelForm):
    
    supervisor = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=OPTIONS)
    # responsible_person = forms.ModelMultipleChoiceField(
    #                         queryset=User.objects.filter(groups__name='A&D'),
    #                         widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Task
        fields = ('name_task', 'project', 'note', 
        'startDate', 'endDate', 'supervisor','status','document')
