from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm
from .forms import CustomRegisterForm  # If you created one
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task
from .forms import TaskForm

# PROFILE VIEW
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

# DASHBOARD VIEW
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

# LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


# REGISTER VIEW

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')

# ADD TASK
@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

# UPDATE TASK
@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'update_task.html', {'form': form})

# DELETE TASK
@login_required
def delete_task(request, pk):  # FIXED: Use pk to match the URL pattern
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('dashboard')
    return render(request, 'delete_task.html', {'task': task})

# COMPLETED TASKS
@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed=True).order_by('-created_at')
    return render(request, 'completed_tasks.html', {'tasks': tasks})

# TASK LIST VIEW
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    pending_tasks = tasks.filter(completed=False).order_by('-created_at')
    completed_tasks = tasks.filter(completed=True).order_by('-created_at')

    context = {
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'pending_count': pending_tasks.count(),
        'completed_count': completed_tasks.count(),
        'total_count': tasks.count()
    }

    return render(request, 'todo/task_list.html', context)
@login_required
def dashboard(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('dashboard')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    pending_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)

    return render(request, 'todo/dashboard.html', {
        'form': form,
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'pending_count': pending_tasks.count(),
        'completed_count': completed_tasks.count(),
        'total_count': tasks.count()
    })