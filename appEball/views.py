import json
from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import View
from .forms import CustomUserForm, CustomUserLoginForm, EditProfileForm,TournamentCreationForm, TeamCreationForm
from .models import CustomUser, Tournament, Team, Tactic, Notification, Player
from django.http import JsonResponse
from django.db import transaction
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if(user.username == "admin"):
                user.isAccepted = True
                user.isTournamentManager = True
                user.save()
            else:
                admin = CustomUser.objects.filter(username="admin")
                n = Notification(text = "New Register!\n"+user.username+" registered.", title = "New Register", user = admin[0])
                n.save()
            n = Notification(text = "Welcome to Eball!\nHere you can play in different teams with different people.\nJust waiting for admin confirmation.", title = "Welcome to Eball!", user = user)
            n.save()
            login(request, user)
            messages.success(request, 'Account created successfuly!')
            return HttpResponseRedirect(reverse('appEball:home_page'))
        else:
            print(form.errors)
            messages.warning(request, f'Form is not valid.')
            return HttpResponseRedirect(reverse('appEball:register'))

class UserLogin(View):
    form_class = CustomUserLoginForm
    template_name = 'appEball/login.html'

    def get(self, request):
        return render(request, self.template_name, {'title': 'Login', 'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('appEball:home_page'))
            else:
                messages.warning(request, 'Invalid username or password.')
                return HttpResponseRedirect('')
        else:
            messages.warning(request, 'Invalid username or password.')
            return HttpResponseRedirect('')

def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('appEball:home_page'))

class teams_list(View):
    form_class = TeamCreationForm
    template_name = 'appEball/teams_list.html'

    def get(self, request):
        tournaments = Tournament.objects.all()
        tactics = Tactic.objects.all()
        allTeamsFilter=list(Team.objects.all())
        allTeams=list()
        myTeams=list()

        if(request.user.is_authenticated):
            myTeamsFilter=list(Player.objects.filter(user=request.user))
        else:
            myTeamsFilter=list()

        f = TeamCreationForm()
        for i in range(len(allTeamsFilter)):
            if(i%2==0):
                allTeams.append(["row2",allTeamsFilter[i]])
                if(len(myTeamsFilter)>i):
                    myTeams.append(["row2",myTeamsFilter[i]])
                    
            else:
                allTeams.append(["row1",allTeamsFilter[i]])
                if(len(myTeamsFilter)>i):
                    myTeams.append(["row1",myTeamsFilter[i]])
        return render(request, 'appEball/teams_list.html', {'allTeams':allTeams, 'myTeams':myTeams, 'tactics':tactics, 'tournaments':tournaments, 'form':f })

    def post(self, request):
        if request.method=="POST":
            form = self.form_class(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                tournament = form.cleaned_data.get('tournament')
                tactic = form.cleaned_data.get('tactic')
                captain = request.user
                newTeam = Team(name=name,tactic=tactic,tournament=tournament,captain=captain, availGK=tactic.nGK, availDF=tactic.nDF, availMF=tactic.nMF, availFW=tactic.nFW, availST=tactic.nST)
                newTeam.save()
                messages.success(request, 'Team created successfuly!')
                return HttpResponseRedirect(reverse('appEball:join_team', kwargs={'teamId':newTeam.pk}))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect('')


class JoinTeam(View):
    sts = None
    fws = None
    mfs = None
    dfs = None
    gks = None
    numSubs=5
    template_name = 'appEball/joinTeam.html'
    subslist = [None] * numSubs

    def get(self, request, teamId):
        team = Team.objects.get(pk=teamId)
        self._getPlayers(team)
        context = {'team':team, 'sts':self.sts, 'fws':self.fws, 'mfs':self.mfs, 'dfs':self.dfs, 'gks':self.gks}
        if (None not in (self.sts or self.fws or self.mfs or self.dfs or self.gks)):
            context['subsList'] = self.subslist
        return render(request, self.template_name, context)

    def post(self, request, teamId):
        team = Team.objects.get(pk=teamId)
        chosenPosition = request.POST['position']
        try:
            player = Player.objects.get(user=request.user)
            player.position = chosenPosition
            player.save()
        except ObjectDoesNotExist:
            newPlayer = Player(position=chosenPosition, balance=10,nrGoals=0,isStarter=True,isSub=False,team=team,user=request.user)
            newPlayer.save()
        return HttpResponseRedirect(reverse('appEball:teams_list'))

    def _getPlayers(self, team):
        self.sts = [None]*team.tactic.nST
        self.fws = [None]*team.tactic.nFW
        self.mfs = [None]*team.tactic.nMF
        self.dfs = [None]*team.tactic.nDF
        self.gks = [None]*team.tactic.nGK
        stsObj = Player.objects.filter(team=team).filter(position='ST')
        fwsObj = Player.objects.filter(team=team).filter(position='FW')
        mfsObj = Player.objects.filter(team=team).filter(position='MF')
        dfsObj = Player.objects.filter(team=team).filter(position='DF')
        gksObj = Player.objects.filter(team=team).filter(position='GK')
        for i in range(len(stsObj)):
            self.sts[i] = stsObj[i]
        for i in range(len(fwsObj)):
            self.fws[i] = fwsObj[i]
        for i in range(len(mfsObj)):
            self.mfs[i] = mfsObj[i]
        for i in range(len(dfsObj)):
            self.dfs[i] = dfsObj[i]
        for i in range(len(gksObj)):
            self.gks[i] = gksObj[i]
        self.subslist[0] = self.sts.pop(len(self.sts)-1)
        self.subslist[1] = self.fws.pop(len(self.fws)-1)
        self.subslist[2] = self.mfs.pop(len(self.mfs)-1)
        self.subslist[3] = self.dfs.pop(len(self.dfs)-1)
        self.subslist[4] = self.gks.pop(len(self.gks)-1)
        

class tournaments(View):
    form_class = TournamentCreationForm
    def get(self,request):
        allTournamentsFilter=list(Tournament.objects.all())
        allTournaments=[]
        myTournaments=[]
        if(request.user.is_authenticated):
            myTournamentsFilter=list(Tournament.objects.filter(user=request.user))
        else:
            myTournamentsFilter=[]
        for i in range(len(allTournamentsFilter)):
            if(i%2==0):
                allTournaments.append(["row2",allTournamentsFilter[i]])
                if(len(myTournamentsFilter)>i):
                    myTournaments.append(["row2",myTournamentsFilter[i]])
            else:
                allTournaments.append(["row1",allTournamentsFilter[i]])
                if(len(myTournamentsFilter)>i):
                    myTournaments.append(["row1",myTournamentsFilter[i]])

        return render(request, 'appEball/tournaments.html', {'allTournaments':allTournaments,'myTournaments':myTournaments,'week':TournamentCreationForm.week})
    
    def post(self,request):
        if request.method=="POST":
            form = self.form_class(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                maxTeams = form.cleaned_data.get('maxTeams')
                beginDate = form.cleaned_data.get('beginDate')
                endDate = form.cleaned_data.get('endDate')
                gameDays = form.cleaned_data.get('gameDays')
                user = CustomUser.objects.get(username=request.user.username)
                newTournament = Tournament(name=name,maxTeams=maxTeams,beginDate=beginDate,endDate=endDate,gameDays=gameDays,user=user)
                newTournament.save()
                messages.success(request, 'Tournament created successfuly!')
                return HttpResponseRedirect(reverse('appEball:tournaments'))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect(reverse('appEball:new_tournament'))

def user_profile(request, username):
    requestedUser = CustomUser.objects.get(username=username)
    print(requestedUser.profileImg.url)
    return render(request, 'appEball/user_profile.html', {'requestedUser':requestedUser})

class edit_user_profile(View):
    form_class = EditProfileForm

    def get(self, request,username):
        requestedUser = CustomUser.objects.get(username=username)
        return render(request, 'appEball/edit_user_profile.html', {'requestedUser':requestedUser,'form':self.form_class})

    def post(self, request,username):
        if request.method=="POST":
            form = self.form_class(request.POST,request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ' Profile edited successfuly!')
                return HttpResponseRedirect(reverse('appEball:userProfile',kwargs= {"username":username}))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect(reverse('appEball:editUserProfile',kwargs= {"username":username}))

def help(request):
	return render(request,'appEball/help.html',{})

def users(request):
    allUsers = list()
    acceptedUsers = list()
    notAcceptedUsers = list()
    tournamentsManagers = list()
    allFilter = list(CustomUser.objects.all().exclude(username="admin").order_by('isAccepted','username'))
    acceptedFilter = list(CustomUser.objects.filter(isAccepted = True).exclude(username="admin").order_by('username'))
    notAcceptedFilter = list(CustomUser.objects.filter(isAccepted = False).exclude(username="admin").order_by('username'))
    tournamentsManagersFilter = list(CustomUser.objects.filter(isTournamentManager = True).exclude(username="admin").order_by('username'))
    for i in range(len(allFilter)):
        if(i%2==0):
            allUsers.append(["row2",allFilter[i]])
            if(i<len(acceptedFilter)):
                acceptedUsers.append(["row2",acceptedFilter[i]])
            if(i<len(notAcceptedFilter)):
                notAcceptedUsers.append(["row2",notAcceptedFilter[i]])
            if(i<len(tournamentsManagersFilter)):
                tournamentsManagers.append(["row2",tournamentsManagersFilter[i]])
        else:
            allUsers.append(["row1",allFilter[i]])
            if(i<len(acceptedFilter)):
                acceptedUsers.append(["row1",acceptedFilter[i]])
            if(i<len(notAcceptedFilter)):
                notAcceptedUsers.append(["row1",notAcceptedFilter[i]])
            if(i<len(tournamentsManagersFilter)):
                tournamentsManagers.append(["row1",tournamentsManagersFilter[i]])

    return render(request,'appEball/users.html',{'allUsers':allUsers,'acceptedUsers':acceptedUsers,'notAcceptedUsers':notAcceptedUsers,'tournamentsManagers':tournamentsManagers})

def accept_user(request, username):
    requestedUser = CustomUser.objects.get(username=username)
    requestedUser.isAccepted = True
    requestedUser.save()
    print("accept")
    n = Notification(text = "You have been accepted to the app! Check the teams in need of an element.\n Hope you enjoy!", title = "You have been accepted to the app!", user = requestedUser)
    n.save()
    return HttpResponseRedirect(reverse('appEball:users'))

def delete_user(request, username):
    CustomUser.objects.get(username=username).delete()
    return HttpResponseRedirect(reverse('appEball:users'))

def delete_team(request, pk):
    Team.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('appEball:teams_list'))

def delete_tournament(request, pk):
    Tournament.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('appEball:tournament_list'))

def is_tournament_manager(request, username):
    requestedUser = CustomUser.objects.get(username=username)
    print("tuorn:",requestedUser.isTournamentManager)
    if(requestedUser.isTournamentManager == True):
        requestedUser.isTournamentManager = False
        n = Notification(text = "You are no more tournaments manager! You can still create and manage teams or play in another tournaments!", title = "You are no more tournaments manager!", user = requestedUser)
        print("nhecas")
    else:
        requestedUser.isTournamentManager = True
        n = Notification(text = "You are now tournaments manager! You can create and manage tournaments!", title = "You are now tournaments manager!", user = requestedUser)
        print("Tornei gestor de torneios")
    requestedUser.save()
    n.save()
    return HttpResponseRedirect(reverse('appEball:users'))

def notifications(request):
    notifications = list()
    notificationsNotSeen = list()
    notificationsFilter = Notification.objects.filter(user = request.user).order_by('isSeen','-date')
    for i in range(len(notificationsFilter)):
        print("olha ue lindo:",notificationsFilter[i].isSeen)
        if(i%2==0):
            notifications.append(["row2","collapseMessage"+str(i),notificationsFilter[i]])
        else:
            notifications.append(["row1","collapseMessage"+str(i),notificationsFilter[i]])
    notificationsNotSeenFilter = Notification.objects.filter(user = request.user, isSeen = False).order_by('isSeen','-date')
    for i in range(len(notificationsNotSeenFilter)):
        if(i%2==0):
            notificationsNotSeen.append(["row2","collapseMessage"+str(i),notificationsNotSeenFilter[i]])
        else:
            notificationsNotSeen.append(["row1","collapseMessage"+str(i),notificationsNotSeenFilter[i]])
    return render(request, 'appEball/notifications.html', {'notifications':notifications,'notificationsNotSeen':notificationsNotSeen})

def is_seen(request, pk):
    if request.user.is_authenticated:
        request_data = json.loads(request.body)
        try:
            with transaction.atomic():
                notification = Notification.objects.get(pk=pk)
                notification.isSeen = request_data.get("isSeen")
                notification.save()
                notifications = list()
                notificationsFilter = Notification.objects.filter(user = request.user).order_by('-date','-isSeen')
                for i in range(len(notificationsFilter)):
                    if(i%2==0):
                        notifications.append(["row2","collapseMessage"+str(i),notificationsFilter[i]])
                    else:
                        notifications.append(["row1","collapseMessage"+str(i),notificationsFilter[i]])
                return JsonResponse({"success": True})
        except IntegrityError as err:
            raise err
    raise Http404

def askSub(request):
    return render(request, 'appEball/askSub.html', {})

def askKick(request):
    return render(request, 'appEball/askKick.html', {})
   
def tournament_info(request):
    return render(request, 'appEball/tournament_info.html', {})

def tournament_teams(request):
    return render(request, 'appEball/tournament_teams.html', {})