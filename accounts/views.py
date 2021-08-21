from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user 

from .models import *
from .forms import CreateUserForm
from django.contrib.auth.models import Group



@unauthenticated_user
def registerPage(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      group = form.cleaned_data['group']
      group.user_set.add(user)
      messages.success(request, f'Account was created for {username}')
      return redirect('login')

  context = {'form': form}
  return render(request, 'users/register.html', context)


@unauthenticated_user
def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.info(request, 'Username or Password is incorrect')

  context = {}
  return render(request, 'users/login.html', context)


def logoutUser(request):
  logout(request)
  return render(request, 'users/logout.html')


@login_required(login_url='login')
def profile(request):
  context = {}
  return render(request, 'users/profile.html', context)
