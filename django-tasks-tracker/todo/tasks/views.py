from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


@login_required
def home(request):
    current_user = request.user

    tasks = Task.objects.filter(user=current_user.id)
    form = TaskForm()
    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def index(request):
    current_user = request.user

    tasks = Task.objects.filter(user=current_user.id)
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            localForm = form.save(commit=False)
            localForm.user = request.user
            localForm.save()
        return redirect('/')
    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)


def updateTask(request, pk):

    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

    if form.is_valid():
        form.save()
        return redirect('/')

    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):

    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request, 'tasks/delete.html', context)
