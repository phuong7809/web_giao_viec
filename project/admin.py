from django.contrib import admin
from .models import Project,Task,User_task


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','IDproject', 'name', 'startDate',
                    'endDate', 'createdby', 'prior')
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_task', 'project', 'startDate',
                    'endDate', 'get_responsible_person')
 

admin.site.register(Project,ProjectAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(User_task)
