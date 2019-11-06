from django.urls import path, include
from django.conf.urls import url
from django.urls import reverse_lazy
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.htm'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('addproject/', views.add_project, name='addproject'),
    path('', views.dashboard, name='home'),
    path('project_list/',views.project_list,name="project_list"),
    # path('', views.project_list, name='home'),
    path('detail_project/<int:id>/', views.detail_pro, name='detail_pro'),
    path('edit_project/<int:pk>/', views.Project_UpdateView.as_view(), name='edit_pro'),
    path('delete_project/<int:pk>/', views.Project_DeleteView.as_view(), name='delete_pro'),
    path('ajax_get_startdate/',views.get_start_date, name='ajax_get_startdate'),
    path('add_task/',views.add_task, name='add_task'),
    path('task_edit/<int:pk>/', views.Update_task_user.as_view(), name='task_edit'),
    path('task_edit_admin/<int:pk>/', views.UpdateTaskAdmin.as_view(), name='task_edit_admin'),
    path('task_delete_admin/<int:pk>/', views.TaskDeleteView.as_view(), name='task_delete_admin'),
    # path('task_list/',views.task_list,name='task_list'),##
    path('task_list_admin/',views.task_list_admin,name='task_list_admin'),
    path('detail_task/<int:id>/', views.detail_task, name='detail_task'),
    path('ajax_get_status/', views.get_status_task, name='ajax_get_status' ),
    url(r'^ajax/search_task/', views.get_task, name="search_task"),
    url(r'^ajax/search_result_task/', views.SearchResultsView.as_view(), name="search_result_task"),
    # path('ajax_get_timeline/', views.get_timeline, name='get_timeline' ),
    url(r'^change_password/$', views.change_password, name='change_password'),
    path('send/',views.send, name='mail'),
    path('ajax/chartjs/',views.chart, name='chart'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.htm'), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.htm'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.htm'),
         name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.htm'), name='password_reset_complete'),
    
]



