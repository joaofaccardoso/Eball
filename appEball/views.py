from django.shortcuts import render

def home_page(request):
    return render(request, 'appEball/home_page.html', {})

def register(request):
    return render(request, 'appEball/register.html', {})

def teams_list(request):
    return render(request, 'appEball/teams_list.html', {})

