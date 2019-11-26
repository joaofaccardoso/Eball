import json
from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import View
from .forms import CustomUserForm, CustomUserLoginForm, EditProfileForm,TournamentCreationForm, TeamCreationForm
from .models import CustomUser, Tournament, Team, Tactic, Notification, Player, Field, GamesDays
from django.http import JsonResponse
from django.db import transaction
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


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

        for i in range(len(allTeamsFilter)):
                if(i%2==0):
                    player = list(Player.objects.filter(team=allTeamsFilter[i],user=request.user))
                    checkPlayer = (len(player) is 0) and (15-len(Player.objects.filter(team=allTeamsFilter[i])))>0
                    allTeams.append(["row2",allTeamsFilter[i],15-len(Player.objects.filter(team=allTeamsFilter[i])),checkPlayer])
                    if(len(myTeamsFilter)>i):
                        myTeams.append(["row2",myTeamsFilter[i],15-len(Player.objects.filter(team=allTeamsFilter[i]))])   
                else:
                    player = list(Player.objects.filter(team=allTeamsFilter[i],user=request.user))
                    checkPlayer = (len(player) is 0) and (15-len(Player.objects.filter(team=allTeamsFilter[i])))>0
                    allTeams.append(["row1",allTeamsFilter[i],15-len(Player.objects.filter(team=allTeamsFilter[i])),checkPlayer])
                    if(len(myTeamsFilter)>i):
                        myTeams.append(["row1",myTeamsFilter[i],15-len(Player.objects.filter(team=allTeamsFilter[i]))])
    
        for i in range(len(allTeams)):
            for j in range (len(myTeamsFilter)):
                if myTeamsFilter[j].team==allTeams[i][1]:
                    allTeams[i].append(1)
                elif ((myTeamsFilter[j].team!=allTeams[i][1]) and (j==len(myTeamsFilter)-1)):
                    allTeams[i].append(0)
        return render(request, 'appEball/teams_list.html', {'allTeams':allTeams,
                                                            'myTeams':myTeams,
                                                            'tactics':tactics,
                                                            'tournaments':tournaments,
                                                            })

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
                newPlayer = Player(position='MF', balance=20,nrGoals=0,isStarter=True,isSub=False,team=newTeam,user=request.user)
                newPlayer.save()
                return HttpResponseRedirect(reverse('appEball:join_team', kwargs={'teamId':newTeam.pk}))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect('')


def team_info(request,teamId):
    team = Team.objects.get(pk=teamId)
    conta=0
    sts = [None]*team.tactic.nST
    fws = [None]*team.tactic.nFW
    mfs = [None]*team.tactic.nMF
    dfs = [None]*team.tactic.nDF
    gks = [None]*team.tactic.nGK
    stsObj = Player.objects.filter(team=team).filter(position='ST')
    fwsObj = Player.objects.filter(team=team).filter(position='FW')
    mfsObj = Player.objects.filter(team=team).filter(position='MF')
    dfsObj = Player.objects.filter(team=team).filter(position='DF')
    gksObj = Player.objects.filter(team=team).filter(position='GK')
    for i in range(len(stsObj)):
        sts[i] = stsObj[i]
    for i in range(len(fwsObj)):
        fws[i] = fwsObj[i]
    for i in range(len(mfsObj)):
        mfs[i] = mfsObj[i]
    for i in range(len(dfsObj)):
        dfs[i] = dfsObj[i]
    for i in range(len(gksObj)):
        gks[i] = gksObj[i]
    context = {'team':team, 'sts':sts, 'fws':fws, 'mfs':mfs, 'dfs':dfs, 'gks':gks}
    #if (None not in (self.sts or self.fws or self.mfs or self.dfs or self.gks)):
    #    context['subsList'] = subslist
    return render(request,'appEball/team_info.html' , context)


class JoinTeam(View):
    sts = None
    fws = None
    mfs = None
    dfs = None
    gks = None
    numSubs=5
    numPlayers = 11
    template_name = 'appEball/joinTeam.html'
    subslist = None
    playersList = None

    def get(self, request, teamId):
        self.subslist = [None] * self.numSubs
        self.playersList = {}
        team = Team.objects.get(pk=teamId)
        self._getPlayers(team)
        context = {'team':team, 'sts':self.sts, 'fws':self.fws, 'mfs':self.mfs, 'dfs':self.dfs, 'gks':self.gks, 'subsList':self.subslist}
        return render(request, self.template_name, context)

    def post(self, request, teamId):
        chosenPosition = None
        team = Team.objects.get(pk=teamId)
        if 'position' in request.POST:
            chosenPosition = request.POST['position']
        else:
            messages.warning(request, 'You need to choose a position!')
            return HttpResponseRedirect('')
        isStarter = True
        isSub=False
        if chosenPosition == 'subST':
            chosenPosition = 'ST'
            isSub = True
            isStarter = False
        elif chosenPosition == 'subFW':
            chosenPosition = 'FW'
            isSub = True
            isStarter = False
        elif chosenPosition == 'subMF':
            chosenPosition = 'MF'
            isSub = True
            isStarter = False
        elif chosenPosition == 'subDF':
            chosenPosition = 'DF'
            isSub = True
            isStarter = False
        elif chosenPosition == 'subGK':
            chosenPosition = 'GK'
            isSub = True
            isStarter = False
        try:
            player = Player.objects.filter(user=request.user).get(team=team)
            player.position = chosenPosition
            player.isSub = isSub
            player.isStarter = isStarter
            player.save()
        except ObjectDoesNotExist:
            newPlayer = Player(position=chosenPosition, balance=0,nrGoals=0,isStarter=isStarter,isSub=isSub,team=team,user=request.user)
            newPlayer.save()
            notification = Notification(title='New Player on '+team.name+'!', text=newPlayer.user.username+' wants to join your team!', user=team.captain)
            notification.save()
        return HttpResponseRedirect(reverse('appEball:teams_list'))

    def _getPlayers(self, team):
        self.sts = []
        self.fws = []
        self.mfs = []
        self.dfs = []
        self.gks = []
        stsObj = Player.objects.filter(team=team).filter(position='ST')
        fwsObj = Player.objects.filter(team=team).filter(position='FW')
        mfsObj = Player.objects.filter(team=team).filter(position='MF')
        dfsObj = Player.objects.filter(team=team).filter(position='DF')
        gksObj = Player.objects.filter(team=team).filter(position='GK')
        for st in stsObj:
            print(st.user.username+'\n ST')
            if st.isSub:
                self.subslist[0] = st
            else:
                self.sts.append(st)
        if len(self.sts) < team.tactic.nST-1:
            self.sts.extend([None]*(team.tactic.nST-1 - len(self.sts)))
        for fw in fwsObj:
            print(fw.user.username+'\n FW')
            if fw.isSub:
                self.subslist[1] = fw
            else:
                self.fws.append(fw)
        if len(self.fws) < team.tactic.nFW-1:
            self.fws.extend([None]*(team.tactic.nFW-1 - len(self.fws)))
        for mf in mfsObj:
            print(mf.user.username+'\n MF')
            if mf.isSub:
                self.subslist[2] = mf
            else:
                self.mfs.append(mf)
        if len(self.mfs) < team.tactic.nMF-1:
            self.mfs.extend([None]*(team.tactic.nMF-1 - len(self.mfs)))
        for df in dfsObj:
            print(df.user.username+'\n DF')
            if df.isSub:
                self.subslist[3] = df
            else:
                self.dfs.append(df)
        if len(self.dfs) < team.tactic.nDF-1:
            self.dfs.extend([None]*(team.tactic.nDF-1 - len(self.dfs)))
        for gk in gksObj:
            print(gk.user.username+'\n GK')
            if gk.isSub:
                self.subslist[4] = gk
            else:
                self.gks.append(gk)
        if len(self.gks) < team.tactic.nGK-1:
            self.gks.extend([None]*(team.tactic.nGK-1 - len(self.gks)))
        print(self.playersList)
        

class tournaments(View):
    form_class = TournamentCreationForm
    def get(self,request):
        allTournamentsFilter=list(Tournament.objects.all())
        allTournaments=[]
        myTournaments=[]
        fields = Field.objects.all()
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

        return render(request, 'appEball/tournaments.html', {'allTournaments':allTournaments,'myTournaments':myTournaments,'week':TournamentCreationForm.week,'fields':fields})
    
    def post(self,request):
        if request.method=="POST":
            form = self.form_class(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                maxTeams = form.cleaned_data.get('maxTeams')
                beginDate = form.cleaned_data.get('beginDate')
                endDate = form.cleaned_data.get('endDate')
                user = CustomUser.objects.get(username=request.user.username)
                newTournament = Tournament(name=name,maxTeams=maxTeams,beginDate=beginDate,endDate=endDate,user=user)

                ok = True
                if(request.POST['gameDays']):
                    gameDays = request.POST['gameDays']
                    print(gameDays)
                else:
                    ok=False
                    messages.warning(request, f'Games days is required')
                
                if(request.POST['field']):
                    field = Field.objects.get(pk=request.POST['field'])
                else:
                    ok=False
                    messages.warning(request, f'Field is required')

                if(request.POST['startHour']):
                    startHour = request.POST['startHour']
                else:
                    ok=False
                    messages.warning(request, f'Start hour is required')

                if(request.POST['endHour']):
                    endHour = request.POST['endHour']
                else:
                    ok=False
                    messages.warning(request, f'End hour is required')  

                if(ok):
                    newTournament.save()
                    gd = GamesDays(tournament=newTournament,endHour=endHour,startHour=startHour,field=field,gameDays=gameDays)
                    gd.save()
                    messages.success(request, 'Tournament created successfuly!')

                return HttpResponseRedirect(reverse('appEball:tournaments'))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect(reverse('appEball:tournaments'))

def user_profile(request, username):
    requestedUser = CustomUser.objects.get(username=username)
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
    return HttpResponseRedirect(reverse('appEball:tournaments'))

def is_tournament_manager(request, username):
    requestedUser = CustomUser.objects.get(username=username)
    if(requestedUser.isTournamentManager == True):
        requestedUser.isTournamentManager = False
        n = Notification(text = "You are no more tournaments manager! You can still create and manage teams or play in another tournaments!", title = "You are no more tournaments manager!", user = requestedUser)
    else:
        requestedUser.isTournamentManager = True
        n = Notification(text = "You are now tournaments manager! You can create and manage tournaments!", title = "You are now tournaments manager!", user = requestedUser)
    requestedUser.save()
    n.save()
    return HttpResponseRedirect(reverse('appEball:users'))

def notifications(request):
    notifications = list()
    notificationsNotSeen = list()
    notificationsFilter = Notification.objects.filter(user = request.user).order_by('isSeen','-date')
    for i in range(len(notificationsFilter)):
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

class tournament_info(View):
    template_name = 'appEball/tournament_info.html'
    def get(self,request,pk):
        #falta buscar o pk certo de quando ele clica no torneio no outro ecra e mandar para aqui      
        tournament=Tournament.objects.get(pk=pk)
        allteams=list(Team.objects.filter(tournament=tournament))
        allDays=list(GamesDays.objects.filter(tournament=tournament))
        days=list()
        teams=list()
        scores=list()
        jogos=list()

        manager=request.user.isTournamentManager

        for i in range(len(allDays)):
            if(i%2==0):
                days.append(["row2",allDays[i]])
            else:
                days.append(["row1",allDays[i]])
        scores=None
        jogos=None

        for i in range(len(allteams)):
            if(i%2==0):
                teams.append(["row1",allteams[i]])
                    
            else:
                teams.append(["row2",allteams[i]])
       
        return render(request, self.template_name, {'tournament':tournament,'teams':teams,'days':days,'Scores':scores,'Jogos':jogos,'manager':manager})

    def post(self, request,pk):
         if request.method=="POST":
            return HttpResponseRedirect(reverse('appEball:join_team', kwargs={'teamId':pk}))

def generate_games(request, pk):
    tournament = Tournament.objects.get(pk=pk)
    teams = Team.objects.filter(tournament=tournament)
    return HttpResponseRedirect(reverse('appEball:tournament_info', kwargs={'pk':pk}))


def my_calendar(request):
        return render(request,'appEball/my_calendar.html',{})
