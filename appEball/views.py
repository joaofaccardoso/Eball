from django.shortcuts import render
from .forms import UserForm

def home_page(request):
    return render(request, 'appEball/home_page.html', {})
    
def navbar(request):
    return render(request, 'appEball/navbar.html', {})

def register(request):
    form = UserForm()
    return render(request, 'appEball/register.html', {'form':form})

def login(request):
    return render(request, 'appEball/login.html', {})

def teams_list(request):
    return render(request, 'appEball/teams_list.html', {})

def user_profile(request):
	return render(request,'appEball/user_profile.html',{})
