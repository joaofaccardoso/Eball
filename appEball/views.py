from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.views import View
from .forms import CustomUserForm, CustomUserLoginForm

class HomePage(View):
    template_name = 'appEball/home_page.html'

    def get(self, request):
        return render(request, self.template_name, {'title': 'Home'})

class UserRegister(View):
    form_class = CustomUserForm
    template_name = 'appEball/register.html'

    def get(self, request):
        return render(request, self.template_name, {'title': 'Register'})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(request, 'Account created successfuly!')
            return HttpResponseRedirect(reverse('appEball:home_page'))
        else:
            messages.warning(request, f'Form is not valid.')
            return HttpResponseRedirect(reverse(self.template_name))

class UserLogin(View):
    form_class = CustomUserLoginForm
    template_name = 'appEball/login.html'

    def get(self, request):
        return render(request, self.template_name, {'title': 'Login'})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome { user.firstName } { user.lastName }!')
                return HttpResponseRedirect(reverse('appEball:home_page'))
            else:
                messages.warning(request, 'Invalid e-mail or password.')
                return HttpResponseRedirect(reverse('appEball:login'))
        else:
            messages.warning(request, 'Invalid e-mail or password.')
            return HttpResponseRedirect(reverse('appEball:login'))

def userLogout(request):
    logout(request)
    messages.warning(request, 'You logged out')
    return HttpResponseRedirect(reverse('appEball:home_page'))

def teams_list(request):
    return render(request, 'appEball/teams_list.html', {})

def user_profile(request):
	return render(request,'appEball/user_profile.html',{})
