from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
 path('', RedirectView.as_view(url='login/', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_task, name='add_task'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),  # FIXED: task_id → pk
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('tasks/', views.task_list, name='task_list'),
    path('profile/', views.profile, name='profile'),

]