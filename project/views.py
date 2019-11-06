from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group, User
from .forms import ProjectForm, TaskForm
from .models import Project, User_task, Task
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.views.generic import TemplateView, ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
import json
import datetime
import schedule
import time

@login_required(login_url='/login/')
def add_project(request):
    user = request.user
    if request.user.has_perm('project.add_project'):
    
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES)
            id_project = Project.objects.values_list('id',flat=True).last()
            id_project = id_project + 1
            if form.is_valid():
                # idproject = request.POST.get('IDproject')
                name = request.POST.get('name')
                startDate = request.POST.get('startDate')

                start = startDate[:10].split('-')
                start01 = ''.join(start)

                endDate = request.POST.get('endDate')
                description = request.POST.get('description')
                prior = request.POST.get('prior')
                participants = request.POST.get('participants')
                crea = user
                idproject = 'DA'+start01+ str(id_project)


                pro = Project()
                pro.IDproject = idproject
                pro.name = name
                pro.startDate = startDate
                pro.endDate = endDate
                pro.createdby = crea
                pro.description = description
                pro.prior = prior
                pro.participants_id = participants
                pro.save()
            # return HttpResponse('Project added to database')
            return redirect("/")
        else:
            form = ProjectForm
        return render(request, 'add_project.htm', {'project_form': form})
    else:
        return render(request,'end.htm')

@login_required(login_url='/login/')
def project_list(request):
    if request.user.is_authenticated:
        user = request.user
        # pros = Project.objects.filter(createdby=user)
        if user.is_superuser:
            pros = Project.objects.all()
            return render(request, 'home.htm', {'pros': pros})
        else:
            # return render(request,'end_user_pro.htm')
            team = list(User.objects.filter(username=user).values_list('groups__name',flat=True))
            pros = Project.objects.filter(participants__name =team[0])
            return render(request,'project_list_user.htm',{'pros':pros})

@login_required(login_url='/login/')
def detail_pro(request, id):
    projects = get_object_or_404(Project, id=id)
    return render(request, 'detail_project.htm', {'projects': projects})

@method_decorator(login_required, name='dispatch')
class Project_UpdateView(UpdateView):
    model = Project
    fields = ['IDproject', 'name', 'startDate',
              'endDate', 'description', 'prior', ]
    template_name = 'edit_project.htm'
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        # here you can make your custom validation for any particular user
        if not request.user.is_superuser:
            # raise PermissionDenied()
            return render(request,'end.htm') 
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class Project_DeleteView(DeleteView):
    model = Project
    template_name = 'delete_pro.htm'
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        # here you can make your custom validation for any particular user
        if not request.user.is_superuser:
            # raise PermissionDenied()
            return render(request,'end.htm') 
        return super().dispatch(request, *args, **kwargs)

@login_required(login_url='/login/')
def add_task(request):
    if request.user.has_perm('project.add_project'):
        id_task = Task.objects.values_list('id').last()[0]
        id_task= id_task +1
        if request.method == 'POST':
            form = TaskForm(request.POST,request.FILES)
            if form.is_valid():
                name_task = request.POST.get('name_task')
                name_project = request.POST.get('project')
                note = request.POST.get('note')
                startDate = request.POST.get('startDate')
                start = startDate[:10].split('-')
                start01 = ''.join(start)
                endDate = request.POST.get('endDate')
                supervisor = request.POST.getlist('supervisor')
                supervisor = ",".join(str(x) for x in supervisor)
                responsible_person = request.POST.getlist('responsible_person')
                print(responsible_person)
                responsible_person = " ,".join(str(x) for x in responsible_person)
                status = request.POST.get('status')
                ID_task = 'CV'+start01+ str(id_task)
                document = request.FILES.get('document')

                task = Task.objects.create(name_task=name_task, project_id =name_project, note=note, 
                                             startDate=startDate, endDate=endDate, supervisor=supervisor,
                                              responsible_person=responsible_person, status=status, ID_task=ID_task, document=document)
                
            return redirect("task_list_admin")
            # return HttpResponse('them task ok')
        else:
            form = TaskForm()
        return render(request, 'add_task.htm', {'form': form })
    else:
        return render(request,'end.htm')
# cho ham add_task
def get_start_date(request):
    if request.is_ajax():
        project_id = request.POST.get('project_id')
        if project_id == "":
            data = {
                'start_date': False,
                'end_date': False
            }
        else:
            query = Project.objects.get(id=project_id)
            users = User.objects.filter(groups__name=query.participants).values_list('username',flat=True)
            # print(users)
            
            data = {
                'start_date': str(query.startDate),
                'end_date': str(query.endDate),
                'group' : str(query.participants),
                'users' : list(users),
            }
        return JsonResponse(data)

@login_required(login_url='/login/')
def task_list_admin(request):
    if request.user.is_authenticated:
        user = request.user
        aa = dict(Task.objects.values_list('name_task','responsible_person'))
        query = request.GET.get('txtsearch')
        time_now = datetime.datetime.now().date()   
        print(time_now)
        li = []
        query2 = list(Task.objects.filter(muc_do_hoan_thanh =100))
        for i in query2:
            new_status = Task.objects.filter(id=i.id).update(status ='Finish')

        if user.is_superuser:
            if query is None or query == '':
                tasks_all = Task.objects.all().order_by('ID_task')
                data = {
                    'tasks_all' : tasks_all,
                    'time_now' : time_now,
                }
            else :
                object_list = Task.objects.filter(ID_task =query) 
                data = {
                    'tasks_all' : object_list,
                    'time_now' : time_now,
                }
            return render(request,'task_list_admin.htm',data)
        else:
            # return render(request,'end.htm')
            for i,j in aa.items():
                if (str(user) in j):
                    li.append(i)
                    tasks_new= Task.objects.filter(Q(name_task__in=li)& Q(status='New'))
                    tasks_process= Task.objects.filter(Q(name_task__in=li)& Q(status='Processing'))
                    tasks_finish= Task.objects.filter(Q(name_task__in=li)& Q(status='Finish'))
                    data = {
                        'tasks_new' : tasks_new,
                        'tasks_process':tasks_process,
                        'tasks_finish' :tasks_finish,
                        'time_now' :time_now,
                    }
            return render(request, 'task_list.htm', data)


# hiển thị task cho user####  có thể bỏ
@login_required(login_url='/login/')
def task_list(request):
    li = []
    query = list(Task.objects.filter(muc_do_hoan_thanh =100))
    time_now = datetime.datetime.now().date()
    # print(query)
    for i in query:
        new_status = Task.objects.filter(id=i.id).update(status ='Finish')

    if request.user.is_authenticated:
        user = request.user
        aa = dict(Task.objects.values_list('name_task','responsible_person'))
        for i,j in aa.items():
            if not user.is_superuser:
                if (str(user) in j):
                    li.append(i)
                    tasks_new= Task.objects.filter(Q(name_task__in=li)& Q(status='New'))
                    tasks_process= Task.objects.filter(Q(name_task__in=li)& Q(status='Processing'))
                    tasks_finish= Task.objects.filter(Q(name_task__in=li)& Q(status='Finish'))
                    data = {
                        'tasks_new' : tasks_new,
                        'tasks_process':tasks_process,
                        'tasks_finish' :tasks_finish,
                        'time_now' : time_now,
                    }
    return render(request, 'task_list.htm', data)

@login_required(login_url='/login/')
def detail_task(request, id):
    tasks = get_object_or_404(Task, id=id)
    return render(request, 'detail_task.htm', {'tasks': tasks})
    # return render(request, 'edit_task.htm', {'tasks': tasks})

# ajax cho ham task_list // hien thi cong viec
@login_required(login_url='/login/')
def get_status_task(request):
    if request.is_ajax() and request.POST:
        status = request.POST.get('status')
        if ('yes' in status):
            status1 = int(''.join(filter(str.isdigit, status)))
            query = Task.objects.get(id=status1)
            # print(query)
            new_status = Task.objects.filter(id=query.id).update(status ='Processing')
            # print(new_status)
            data = {
                'name_task' : query.id,
                'name' : new_status,
            }
            # print(data)
        else:
            status2 = int(''.join(filter(str.isdigit, status)))
            query = Task.objects.get(id=status2)
            # print(query)
            new_status = Task.objects.filter(id=query.id).update(status ='Reject')
            # print(new_status)
            data = {
                'name_task2' : query.id,
                'name2' : new_status,
            }
        return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class get_search_task(ListView):
    model = Task
    context_object_name = 'list_task'
    template_name = 'task_list_admin.htm'
    
    def get_queryset(self): 
        query = self.request.GET.get('txtsearch')
        #print(query)
        object_list = Task.objects.filter(
            Q(ID_task__icontains=query) 
            )
       # print(object_list)
        return object_list
    
# cho task_list_Admin_search
def get_task(request):
    if request.is_ajax():
        li=[]
        name_task = dict(Task.objects.values_list('id','ID_task'))
        for i,j in name_task.items():
            li.append(j)
        # print(li)
        data ={
            'name_task' : li
        }
    return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class SearchResultsView(ListView):
    model = Task
    context_object_name = 'list_task'
    template_name = 'search_task.htm'
    
    def get_queryset(self): 
        query = self.request.GET.get('txtsearch')
        print(query)
        object_list = Task.objects.filter(ID_task =query)
        print(object_list)
        return object_list

@login_required(login_url='/login/')
def dashboard(request):
    user = request.user
    print(type(user))
    aa = dict(Task.objects.values_list('name_task','responsible_person'))
    li = []
    if user.is_superuser :
        count_task_new = Task.objects.filter(status ='New').count()
        count_task_process = Task.objects.filter(status ='Processing').count()
        count_task_finish = Task.objects.filter(status ='Finish').count()
        count_task_reject = Task.objects.filter(status ='Reject').count()
        data = {
            'count_task_new' : count_task_new,
            'count_task_process' : count_task_process,
            'count_task_finish' : count_task_finish,
            'count_task_reject' : count_task_reject,
        }
    else:
        for i,j in aa.items():
            if str(user) in j:
                li.append(i)
                count_task_new = Task.objects.filter(Q(name_task__in=li)& Q(status='New')).count()
                count_task_process = Task.objects.filter(Q(name_task__in=li)& Q(status='Processing')).count()
                count_task_finish = Task.objects.filter(Q(name_task__in=li)& Q(status='Finish')).count()
                count_task_reject = Task.objects.filter(Q(name_task__in=li)& Q(status='Reject')).count()
                data = {
                    'count_task_new' : count_task_new,
                    'count_task_process':count_task_process,
                    'count_task_finish': count_task_finish,
                    'count_task_reject' :count_task_reject,
                }
    return render(request,'dashboard.html',data)

@method_decorator(login_required, name='dispatch')
class Update_task_user(UpdateView):
    model = Task
    fields = ('note', 'muc_do_hoan_thanh','document')
    template_name = 'edit_task.htm'
    success_url = reverse_lazy('task_list_admin')

    def dispatch(self, request, *args, **kwargs):
        # here you can make your custom validation for any particular user
        if not request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # return HttpResponse('admin k dc sua')
        return redirect('task_list_admin')

class UpdateTaskAdmin(UpdateView):
    model = Task
    fields = ('endDate',)
    template_name = 'edit_task_admin.htm'
    success_url = reverse_lazy('task_list_admin')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request,'end.htm') 
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete_task.htm'
    success_url = reverse_lazy('task_list_admin')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            # raise PermissionDenied()
            return render(request,'end.htm') 
        return super().dispatch(request, *args, **kwargs)

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.htm', {'form': form})


@login_required(login_url='/login/')
def send(request):
    person1 = []
    li2=[]
    now=datetime.datetime.now().date()
    end_date = list(Task.objects.values_list('endDate','responsible_person'))
    for i in end_date:
        date = str(i[0].date()-now).split()[0]
        if date == '1':
            person1.append(i[1])
            str1=','.join(person1)
            bn=list(set(list(str1.split(","))))
            bv=list(User.objects.values_list('username','email'))
            for n in bv:
                for m in bn:
                    if n[0] in m:
                        li2.append(n[1])
            li2=list(set(li2))
            res = send_mail('Thông báo hạn dealine',
            'Công việc bạn đang thực hiện ngày mai sẽ hết hạn.Hãy hoàn thành công việc sớm.',
            'phuonglang0611bg@gmail.com',
            li2,
            fail_silently = False )
            return HttpResponse('ok')
    # return render(request,'send_mail.htm')   

# schedule.every(5).minutes.do(send)
# schedule.every().hour.do(send)
# schedule.every().day.at("10:30").do(send)
# schedule.every(5).to(10).minutes.do(send)
# schedule.every().monday.do(send)
# schedule.every().wednesday.at("13:15").do(send)
# schedule.every().minute.at(":17").do(send)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

@login_required(login_url='/login/')
def chart(request):
    user = request.user
    processing = []
    processing2 = []
    finish = []
    finish2 = []
    if not user.is_superuser :
        team = list(User.objects.filter(username=user).values_list('groups__name',flat=True))
        all_user_team = list(User.objects.filter(groups__name=team[0]).values_list('username',flat=True))
        for i in all_user_team:
            task_processing = Task.objects.filter(responsible_person__contains=i,status='Processing').count()
            processing.append(task_processing)
            task_finish = Task.objects.filter(responsible_person__contains=i,status='Finish').count()
            finish.append(task_finish)
        data = {
            'label' : all_user_team ,
            'task_processing' : processing,
            'task_finish' : finish,
        }
        
    else:
        all_user_team = list(User.objects.values_list('username',flat=True))
        for i in all_user_team:
            task_processing = Task.objects.filter(responsible_person__contains=i,status='Processing').count()
            processing2.append(task_processing)
            task_finish = Task.objects.filter(responsible_person__contains=i,status='Finish').count()
            finish2.append(task_finish)
        data = {
            'label' : all_user_team,
            'task_processing' : processing2,
            'task_finish' : finish2,
        }
    return JsonResponse(data)
        # return HttpResponse()
    # return render(request,'dashboard.html',data)
