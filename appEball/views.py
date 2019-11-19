from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.views import View
from .forms import CustomUserForm, CustomUserLoginForm, EditProfileForm,TournamentCreationForm, TeamCreationForm
from .models import CustomUser, Tournament, Team

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
            return HttpResponseRedirect(reverse('appEball:register'))

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
                return HttpResponseRedirect(reverse('appEball:home_page'))
            else:
                messages.warning(request, 'Invalid e-mail or password.')
                return HttpResponseRedirect(reverse('appEball:login'))
        else:
            messages.warning(request, 'Invalid e-mail or password.')
            return HttpResponseRedirect(reverse('appEball:login'))

def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('appEball:home_page'))

def teams_list(request):
    teams_initial=list(Team.objects.all())
    teams=[]
    for i in range(len(teams_initial)):
        print("oi")
        if(i%2==0):
            teams.append(["row2",teams_initial[i]])
        else:
            teams.append(["row1",teams_initial[i]])

    return render(request, 'appEball/teams_list.html', {'teams_list':teams})




class new_team(View):
    form_class = TeamCreationForm
    template_name = 'appEball/new_team.html'

    def get(self, request):
        return render(request, self.template_name,{'tactics':TeamCreationForm.tacticChoice})

    def post(self, request):
        if request.method=="POST":
            form = self.form_class(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Team created successfuly!')
                return HttpResponseRedirect(reverse('appEball:teams_list'))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect(reverse('appEball:new_team'))

def tournaments(request):
    tournaments_initial=list(Tournament.objects.all())
    tournaments=[]
    for i in range(len(tournaments_initial)):
        if(i%2==0):
            tournaments.append(["row2",tournaments_initial[i]])
        else:
            tournaments.append(["row1",tournaments_initial[i]])

    return render(request, 'appEball/tournaments.html', {'tournaments':tournaments})


def user_profile(request, username):
	requestedUser = CustomUser.objects.get(username=username)
	return render(request, 'appEball/user_profile.html', {'requestedUser':requestedUser})

class edit_user_profile(View):
    form_class = EditProfileForm

    def get(self, request,username):
        print("ALO")
        requestedUser = CustomUser.objects.get(username=username)
        return render(request, 'appEball/edit_user_profile.html', {'requestedUser':requestedUser})

    def post(self, request,username):
        print("oi1")
        if request.method=="POST":
            form = self.form_class(data=request.POST, instance=request.user)
            if form.is_valid():
                print("oi2")
                user=form.save()

                username = form.cleaned_data.get('username')
                messages.success(request, ' Profile edited successfuly!')
                return HttpResponseRedirect(reverse('appEball:userProfile',kwargs= {"username":username}))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect(reverse('appEball:editUserProfile',kwargs= {"username":username}))

def help(request):
	return render(request,'appEball/help.html',{})



def users(request):
    acceptedUsers = list()
    notAcceptedUsers = list()
    tournamentsManagers = list()
    acceptedFilter = list(CustomUser.objects.filter(isAccepted = True).exclude(username="admin").order_by('username'))
    notAcceptedFilter = list(CustomUser.objects.filter(isAccepted = False).exclude(username="admin").order_by('username'))
    tournamentsManagersFilter = list(CustomUser.objects.filter(isTournamentManager = True).exclude(username="admin").order_by('username'))

    for i in range(len(acceptedFilter)):
        print(acceptedFilter[i].username)
        if(i%2==0):
            acceptedUsers.append(["row2",acceptedFilter[i]])
        else:
            acceptedUsers.append(["row1",acceptedFilter[i]])
    for i in range(len(notAcceptedFilter)):
        if(i%2==0):
            notAcceptedUsers.append(["row2",notAcceptedFilter[i]])
        else:
            notAcceptedUsers.append(["row1",notAcceptedFilter[i]])
    for i in range(len(tournamentsManagersFilter)):
        if(i%2==0):
            tournamentsManagers.append(["row2",tournamentsManagersFilter[i]])
        else:
            tournamentsManagers.append(["row1",tournamentsManagersFilter[i]])
    return render(request,'appEball/users.html',{'acceptedUsers':acceptedUsers,'notAcceptedUsers':notAcceptedUsers,'tournamentsManagers':tournamentsManagers})

def accept_user(request, username):
    requestedUser = CustomUser.objects.get(username=username)
    requestedUser.isAccepted = True
    requestedUser.save()
    return HttpResponseRedirect(reverse('appEball:users'))

def delete_user(request, username):
    CustomUser.objects.get(username=username).delete()
    return HttpResponseRedirect(reverse('appEball:users'))

def is_tournament_manager(request, username):
    requestedUser = CustomUser.objects.get(username=username)
    if(requestedUser.isTournamentManager):
        requestedUser.isTournamentManager = False
    else:
        requestedUser.isTournamentManager = True
    requestedUser.save()
    return HttpResponseRedirect(reverse('appEball:users'))



class new_tournament(View):
    form_class = TournamentCreationForm
    template_name = 'appEball/new_tournament.html'

    def get(self, request):
        return render(request, self.template_name,{'week':TournamentCreationForm.week})

    def post(self, request):
        if request.method=="POST":
            form = self.form_class(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tournament created successfuly!')
                return HttpResponseRedirect(reverse('appEball:tournaments'))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect(reverse('appEball:new_tournament'))