import json
import random
import datetime
from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import View
from .forms import CustomUserForm, CustomUserLoginForm, EditProfileForm, TeamCreationForm, TournamentDaysForm,ReserveForm, SubForm, GameForm
from .models import CustomUser, Tournament, Team, Tactic, Notification, Player, Field, Game, Reserve, Substitute, Slot, Result
from django.http import JsonResponse
from django.db import transaction
from django.db import IntegrityError
from operator import attrgetter
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


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
                admin = CustomUser.objects.get(username="admin")
                n = Notification(text = "New Register!\n"+user.username+" registered.", title = "New Register", user = admin)
                n.save()
            n = Notification(text = "Welcome to Eball!\nHere you can play in different teams with different people.\nJust waiting for admin confirmation.", title = "Welcome to Eball!", user = user)
            n.save()
            login(request, user)
            messages.success(request, 'Account created successfuly!')
            return HttpResponseRedirect(reverse('appEball:home_page'))
        else:
            print(form.errors)
            messages.warning(request, 'Password needs to be at least 8 chars long or passwords do not match!')
            context = {'title': 'Register', 'firstName': form.cleaned_data.get('firstName'), 'lastName':form.cleaned_data.get('lastName'), 'username':form.cleaned_data.get('username'), 'email':form.cleaned_data.get('email'), 'ccNumber':form.cleaned_data.get('ccNumber'),'phoneNumber':form.cleaned_data.get('phoneNumber')}
            return render(request, self.template_name, context)

class UserLogin(View):
    form_class = CustomUserLoginForm
    template_name = 'appEball/login.html'

    def get(self, request):
        return render(request, self.template_name, {'title': 'Login'})

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
                return HttpResponseRedirect(reverse('appEball:login'))
        else:
            messages.warning(request, 'Invalid username or password.')
            return HttpResponseRedirect(reverse('appEball:login'))

def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('appEball:home_page'))

class teams_list(View):
    form_class = TeamCreationForm
    template_name = 'appEball/teams_list.html'

    def get(self, request):
        tactics = Tactic.objects.all()
        allTeamsFilter=list(Team.objects.all().exclude(isDayOff=True))
        allTeams=list()
        myTeams=list()
        tournaments = list()
        myTeamsList=list()
        myTeamsFilter=list()
        myTournaments=list()

        if(request.user.is_authenticated):
            myTeamsList=Player.objects.filter(user=request.user).values_list('team',flat=True)
            myTeamsFilter=Team.objects.filter(pk__in=myTeamsList)
            myTournaments = myTeamsFilter.values_list('tournament',flat=True)
            tournaments = Tournament.objects.all().exclude(pk__in=myTournaments)
            myTeamsFilter=list(myTeamsFilter)
        else:
            tournaments=list(Tournament.objects.all())
            myTeamsFilter=list()

        for i in range(len(allTeamsFilter)):  #ALGUMA COISA DE MAL SE A PESSOA NAO ESTIVER EM NENHUMA EQUIPA
            if(i%2==0):
                if(request.user.is_authenticated):
                    player = list(Player.objects.filter(team=allTeamsFilter[i],user=request.user))
                    checkPlayer = (len(player) == 0) and (16-len(Player.objects.filter(team=allTeamsFilter[i])))>0
                else:
                    checkPlayer = None
                allTeams.append(["row2",allTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),checkPlayer])
                
                if(len(myTeamsFilter)>i and myTeamsFilter[i].isDayOff==False):
                    t_games=(Game.objects.filter(team1=myTeamsFilter[i]) | Game.objects.filter(team2=myTeamsFilter[i])).order_by('slot__date')

                    for j in range (len(t_games)):
                        if t_games[j].slot.date>=timezone.now():
                            myTeams.append(["row2",myTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),t_games[j]])
                            break
                        if (j==len(t_games)-1):
                            myTeams.append(["row2",myTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),0])   
                
                    if (len(t_games)==0):
                        myTeams.append(["row2",myTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),1])
            else:
                if(request.user.is_authenticated):
                    player = list(Player.objects.filter(team=allTeamsFilter[i],user=request.user))
                    checkPlayer = (len(player) == 0) and (16-len(Player.objects.filter(team=allTeamsFilter[i])))>0
                else:
                    checkPlayer = None
                allTeams.append(["row1",allTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),checkPlayer])
                if(len(myTeamsFilter)>i and myTeamsFilter[i].isDayOff==False):
                    t_games=list((Game.objects.filter(team1=myTeamsFilter[i]) | Game.objects.filter(team2=myTeamsFilter[i])).order_by('slot__date'))
                    for j in range (len(t_games)):
                        if t_games[j].slot.date>=timezone.now():
                            myTeams.append(["row1",myTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),t_games[j]])
                            break
                        if (j==len(t_games)-1):
                            myTeams.append(["row1",myTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),0])   
                    if (len(t_games)==0):
                        myTeams.append(["row1",myTeamsFilter[i],16-len(Player.objects.filter(team=allTeamsFilter[i])),1])
    
        return render(request, 'appEball/teams_list.html', {'allTeams':allTeams,
                                                            'myTeams':myTeams,
                                                            'tactics':tactics,
                                                            'myTournaments':myTournaments,
                                                            'myTeamsList':myTeamsList,
                                                            'tournaments':tournaments
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
                newTeam.availMF -= 1
                newTeam.save()
                return HttpResponseRedirect(reverse('appEball:team_info', kwargs={'teamId':newTeam.pk}))
            else:
                print(form.errors)
                messages.warning(request, f'Form is not valid.')
                return HttpResponseRedirect('')

class TeamInfo(View):
    numSubs=5
    template_name = 'appEball/team_info.html'
    subslist = None
    playersList = None
    inTeam = None
    isFull = None

    def get(self, request, teamId):
        self.inTeam = False
        self.isFull = False
        team = Team.objects.get(pk=teamId)
        self._getPlayers(team, request.user)
        player = Player.objects.filter(team=team,user=request.user)
        if (player.count()==0):
            player = None
        else:
            player = player.first()
        context = {'player':player,'team':team, 'tactic':team.tactic.name,'playersList': self.playersList, 'subsList':self.subslist, 'inTeam':self.inTeam, 'isFull':self.isFull}
        return render(request, self.template_name, context)

    def post(self, request, teamId):
        chosenPosition = None
        team = Team.objects.get(pk=teamId)
        if 'position' in request.POST:
            chosenPosition = request.POST['position']
        else:
            messages.warning(request, 'You need to choose a position!')
            return HttpResponseRedirect(reverse('appEball:team_info'))
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
            if player.position == 'ST':
                team.availST = team.availST + 1
            elif player.position == 'FW':
                team.availFW = team.availFW + 1
            elif player.position == 'MF':
                team.availMF = team.availMF + 1
            elif player.position == 'DF':
                team.availDF = team.availDF + 1
            else:
                team.availGK = team.availGK + 1
            if chosenPosition == 'ST':
                team.availST = team.availST - 1
            elif chosenPosition == 'FW':
                team.availFW = team.availFW - 1
            elif chosenPosition == 'MF':
                team.availMF = team.availMF - 1
            elif chosenPosition == 'DF':
                team.availDF = team.availDF - 1
            else:
                team.availGK = team.availGK - 1
            player.position = chosenPosition
            player.isSub = isSub
            player.isStarter = isStarter
            player.save()
            team.save()
        except ObjectDoesNotExist:
            if chosenPosition == 'ST':
                team.availST = team.availST - 1
            elif chosenPosition == 'FW':
                team.availFW = team.availFW - 1
            elif chosenPosition == 'MF':
                team.availMF = team.availMF - 1
            elif chosenPosition == 'DF':
                team.availDF = team.availDF - 1
            else:
                team.availGK = team.availGK - 1
            newPlayer = Player(position=chosenPosition, balance=0,nrGoals=0,isStarter=isStarter,isSub=isSub,team=team,user=request.user)
            newPlayer.save()
            notification = Notification(title='New Player on '+team.name+'!', text=newPlayer.user.username+' joined your team!', user=team.captain)
            notification.save()
            team.save()
        return HttpResponseRedirect(reverse('appEball:teams_list'))

    def _getPlayers(self, team, user):
        sts = []
        fws = []
        mfs = []
        dfs = []
        gks = []
        self.playersList = []
        self.subslist = []
        self.subslist.append([None, 'ST'])
        self.subslist.append([None, 'FW'])
        self.subslist.append([None, 'MF'])
        self.subslist.append([None, 'DF'])
        self.subslist.append([None, 'GK'])
        stsObj = Player.objects.filter(team=team).filter(position='ST')
        fwsObj = Player.objects.filter(team=team).filter(position='FW')
        mfsObj = Player.objects.filter(team=team).filter(position='MF')
        dfsObj = Player.objects.filter(team=team).filter(position='DF')
        gksObj = Player.objects.filter(team=team).filter(position='GK')
        if user.is_authenticated:    
            try:
                player = Player.objects.filter(team = team).get(user = user)
                if player in stsObj or player in fwsObj or player in mfsObj or player in dfsObj or player in gksObj:
                    self.inTeam = True
            except ObjectDoesNotExist:
                pass
        if not (stsObj.count() + fwsObj.count() + mfsObj.count() + dfsObj.count() + gksObj.count()) < 16:
            self.isFull = True
        for st in stsObj:
            if st.isSub:
                self.subslist[0] = [st, st.position]
            else:
                sts.append([st, st.position])
        if len(sts) < team.tactic.nST-1:
            for i in range(team.tactic.nST-1 - len(sts)):
                sts.append([None, 'ST'])
        for fw in fwsObj:
            if fw.isSub:
                self.subslist[1] = [fw, fw.position]
            else:
                fws.append([fw, fw.position])
        if len(fws) < team.tactic.nFW-1:
            for i in range(team.tactic.nFW-1 - len(fws)):
                fws.append([None, 'FW'])
        for mf in mfsObj:
            if mf.isSub:
                self.subslist[2] = [mf, mf.position]
            else:
                mfs.append([mf, mf.position])
        if len(mfs) < team.tactic.nMF-1:
            for i in range(team.tactic.nMF-1 - len(mfs)):
                mfs.append([None, 'MF'])
        for df in dfsObj:
            if df.isSub:
                self.subslist[3] = [df, df.position]
            else:
                dfs.append([df, df.position])
        if len(dfs) < team.tactic.nDF-1:
            for i in range(team.tactic.nDF-1 - len(dfs)):
                dfs.append([None, 'DF'])
        for gk in gksObj:
            if gk.isSub:
                self.subslist[4] = [gk, gk.position]
            else:
                gks.append([gk, gk.position])
        if len(gks) < team.tactic.nGK-1:
            for i in range(team.tactic.nGK-1 - len(gks)):
                gks.append([None, 'GK'])
        self.playersList = sts
        self.playersList.extend(fws)
        self.playersList.extend(mfs)
        self.playersList.extend(dfs)
        self.playersList.extend(gks)
        

class tournaments(View):
    form_class = TournamentDaysForm
    def get(self,request):

        allTournamentsFilter=list(Tournament.objects.all())
        allTournaments=[]
        myTournaments=[]
        fieldsFilter = list(Field.objects.all())
        #self._create_slots(fieldsFilter) 
        fields=list()

        week={0:'Sun',1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'}

        for i in range(len(fieldsFilter)):
            if(i%2==0):
                fields.append(["row1","collapse"+str(fieldsFilter[i].pk),fieldsFilter[i],i==0,i==len(fieldsFilter)-1,[]])
                for j in range(7):
                    fields[i][5].append([week[j],Slot.objects.filter(field=fieldsFilter[i],weekDay=j,tournament=None,date=None).order_by('start')])
            else:
                fields.append(["row2","collapse"+str(fieldsFilter[i].pk),fieldsFilter[i],i==0,i==len(fieldsFilter)-1,[]])
                for j in range(7):
                    fields[i][5].append([week[j],Slot.objects.filter(field=fieldsFilter[i],weekDay=j,tournament=None,date=None).order_by('start')])
        
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
       
        return render(request, 'appEball/tournaments.html', {'allTournaments':allTournaments,'myTournaments':myTournaments,'week':TournamentDaysForm.week,'fields':fields})
    
    def _create_slots(self,fields):
        for f in fields:
            for i in range(7):
                for j in range(16,24):
                    start=datetime.time(j,0,0)
                    end=datetime.time((j+1)%24,0,0)
                    slot=Slot.objects.create(field=f,weekDay=i,start=start,end=end)

    def post(self,request):
        if request.method=="POST":
            form = self.form_class(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                maxTeams = form.cleaned_data.get('maxTeams')
                beginDate = form.cleaned_data.get('beginDate')

                user = CustomUser.objects.get(username=request.user.username)
                newTournament = Tournament(name=name,maxTeams=maxTeams,beginDate=beginDate,user=user)
                newTournament.save()

                tournamentSlots = list()

                fields = request.POST.getlist('gameDays')
                i=0
                while(i<len(fields)):
                    pk=int(fields[i])
                    slot=Slot.objects.get(pk=pk)
                    newSlot=Slot(field=slot.field,weekDay=slot.weekDay,start=slot.start,end=slot.end,tournament=newTournament)

                    slot2=None
                    if(i+1<len(fields)):
                        pk2=int(fields[i+1])
                        slot2=Slot.objects.get(pk=pk2)

                    if(slot2==None):
                        newTournament.delete()
                        messages.warning(request, "You need to choose at least 2 slots together.")
                        return HttpResponseRedirect(reverse('appEball:tournaments'))
                    else:
                        while(slot2.weekDay==slot.weekDay and slot2.start==slot.end):
                            newSlot.end=slot2.end 

                            i+=1
                            slot=slot2
                            if(i+1<len(fields)):
                                pk=int(fields[i+1])
                                slot2=Slot.objects.get(pk=pk)
                            else:
                                break
                        i+=1
                        tournamentSlots.append(newSlot)
                        newSlot.save()
                        print(newSlot)

                messages.success(request, 'Tournament created successfuly!')

                return HttpResponseRedirect(reverse('appEball:tournaments'))
            else:
                for i in form.errors.as_data():
                    for j in form.errors.as_data()[i]:
                        for k in j:
                            if(k=="This field is required."):
                                messages.warning(request, i+" is required.")
                            else:
                                messages.warning(request, k)

                return HttpResponseRedirect(reverse('appEball:tournaments'))

def user_profile(request, username):
    requestedUser = CustomUser.objects.get(username=username)
    myTeamsPk = Player.objects.filter(user=requestedUser).values_list('team',flat=True)
    myTeams = Team.objects.filter(pk__in=myTeamsPk)
    nextGame = (Game.objects.filter(team1__in=myTeams,slot__date__gte=timezone.now()) | Game.objects.filter(team2__in=myTeams,slot__date__gte=timezone.now())).order_by('slot__date').first()
    return render(request, 'appEball/user_profile.html', {'requestedUser':requestedUser,'nextGame':nextGame})

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

class askSub(View):
    def get(self,request,pk):
        tournament=Tournament.objects.get(pk=pk)
        reservest=list(Reserve.objects.filter(tournament=tournament))
        checkr=[]
        subbed=None
        if request.user.is_authenticated:
            checkr=list(Reserve.objects.filter(user=request.user))
            subbed=Player.objects.filter(user=request.user).filter(isSubbed=True)
        check=0
        if (len(checkr)==0):
            check=1 #not reserva
        activeSubs=Substitute.objects.all()

        reserves=[]

        for i in range (len(reservest)):
            if activeSubs.filter(reserveSub=reservest[i]):
                reserves.append([reservest[i],"row2",1])
            else:
                if subbed:
                    reserves.append([reservest[i],"row2",1])
                else:
                    reserves.append([reservest[i],"row2",0])
                
        for i in range(len(reserves)):
            if i%2==0:
                reserves[i][1]="row1"


        return render(request, 'appEball/askSub.html', {'reserves':reserves, 'tournament': tournament, 'check':check})

    def post(self,request,pk):
        if 'sub' in request.POST:
            nGames = request.POST.get('nGames')

            if(nGames==''):
                messages.warning(request, 'You need to put how many games you want a substitute!')
                return HttpResponseRedirect(reverse('appEball:askSub',kwargs={'pk':pk}))

            reservePk = request.POST.get('sub')
            print(reservePk)
            reserve = Reserve.objects.get(pk=reservePk)

            tournament=Tournament.objects.get(pk=pk)
            player = Player.objects.get(team__tournament = tournament,user=request.user)

            player.isSubbed = True
            player.subGames = nGames
            player.save()
            
            substitute = Substitute(originalPlayer = player,reserveSub=reserve)
            substitute.save()            
            
            notification = Notification(title='Requested for you to sub on tournament'+tournament.name+'!', text=player.user.username+' asked you to sub in his next '+ str(nGames) +' games! ' , user=reserve.user)
            notification.save()
        else:
            reservePk = request.POST.get('permanently')
            reserve = Reserve.objects.get(pk=reservePk)

            tournament=Tournament.objects.get(pk=pk)
            player = Player.objects.get(team__tournament = tournament,user=request.user)
            if(player.isStarter):
                playerSub = Player.objects.get(team__tournament = tournament,team=player.team,position = player.position,isSub=True)
                playerSub.isSub = False
                playerSub.isStarter = True
                playerSub.save()
            
            playerReserve = Player(position = player.position,isSub=True,team=player.team,user = reserve.user)
            playerReserve.save()


            notification = Notification(title='Requested for you to sub on team'+playerReserve.team.name+'!', text=player.user.username+' asked you to sub permanently! ' , user=playerReserve.user)
            notification.save()

            reserve.delete()
            player.delete()
        return HttpResponseRedirect(reverse('appEball:askSub',kwargs={'pk':pk}))


def askKick(request):
    return render(request, 'appEball/askKick.html', {})

class tournament_info(View):
    def get(self,request,pk,gRound):
        tournament=Tournament.objects.get(pk=pk)
        if(tournament.gRound==0):
            allTeams=Team.objects.filter(tournament=tournament).order_by('name')
            allTeams=list(allTeams)
            nCompleteTeams = Team.objects.filter(tournament=tournament).filter(availDF=0,availFW=0,availGK=0,availMF=0,availST=0).count()
        else:
            allTeams=list(Team.objects.filter(tournament=tournament).exclude(isDayOff=True).order_by('-points','-goalsDif'))

        
        allDays=list(Slot.objects.filter(tournament=tournament))
        games=list()
        days=list()
        teams=list()

        for i in range(len(allTeams)):
            if(i%2==0):
                teams.append(["row1",allTeams[i]])
            else:
                teams.append(["row2",allTeams[i]])

        for i in allDays:
            if(len(days)%2==0):
                days.append(["row2",i,TournamentDaysForm.week[i.weekDay][1]])
            else:
                days.append(["row1",i,TournamentDaysForm.week[i.weekDay][1]])
                
        gamesRound = list(Game.objects.filter(tournament=tournament,gRound=gRound,team1__in=allTeams,team2__in=allTeams))
        for i in range(len(gamesRound)):
            if(i%2==0):
                games.append(["row2",gamesRound[i]])
            else:
                games.append(["row1",gamesRound[i]])
        
        if(len(list(Game.objects.filter(tournament=tournament).order_by('gRound')))!=0):
            maxRound = list(Game.objects.filter(tournament=tournament).order_by('gRound'))[-1].gRound
        else:
            maxRound=0
        
    
        myTeamsList=list()
        myTournaments = list()
        inTeam=False
        inTournament=False
        if(request.user.is_authenticated):
            myTeamsList=Player.objects.filter(user=request.user).values_list('team',flat=True)
            myTeamsFilter=Team.objects.filter(pk__in=myTeamsList)
            myTournaments = myTeamsFilter.values_list('tournament',flat=True)
            if len(list(myTeamsFilter.filter(tournament=tournament)))!=0 :
                inTeam=True

            myReservesFilter = Reserve.objects.filter(user=request.user).values_list('tournament',flat=True)
            myTournaments=Tournament.objects.filter(pk__in=myReservesFilter)
            if(len(list(myTournaments))>0):
                inTournament = True
        else:
            inTeam= True
    
        return render(request, 'appEball/tournament_info.html', {'tournament':tournament,'inTeam': inTeam,'inTournament': inTournament,'teams': teams,'days':days,'games':games,'gRound':gRound,'plus':'plus','less':'less','maxRound':maxRound,'myTeamsList':myTeamsList,'myTournamentsList':myTournaments})




    def post(self,request,pk,gRound):
        tournament = Tournament.objects.get(pk=pk)
        if request.method=="POST":
            if request.user.is_authenticated:
                if (not Reserve.objects.filter(user=request.user)):
                    form=ReserveForm(request.POST,request.FILES, instance=request.user)
                    reserve=Reserve(user=request.user,tournament=tournament)
                    reserve.save()
            return HttpResponseRedirect(reverse('appEball:askSub',kwargs={'pk': pk}))



def generate_games(request, pk):
    tournament = Tournament.objects.get(pk=pk)
    tournamentSlots = list(Slot.objects.filter(tournament=tournament))

    games=list()
    teams1 = list(Team.objects.filter(tournament=tournament).exclude(isDayOff=True))
    random.shuffle(teams1)

    nTeams = len(teams1)
    nRounds = nTeams-1+nTeams%2
    nGames = nRounds*(nTeams//2+nTeams%2)

    slots=get_slots(tournament.beginDate,nGames,tournamentSlots)

    teams2 = teams1.copy()
    teams2.reverse()
    teams1=teams1[:nTeams//2]
    teams2=teams2[:nTeams//2+nTeams%2]
    
    if(nTeams%2==1):
        tactic=Tactic.objects.get()
        u=list(CustomUser.objects.filter(username=""))
        if(u==[]):
            u=CustomUser(email="",firstName="",lastName="",ccNumber=00000000,phoneNumber=000000000)
            u.save()
        else:
            u=u[0]
        newTeam = Team(name="", tactic=tactic, tournament=tournament, captain=u, isDayOff=True)
        newTeam.save()
        teams1.append(newTeam)

    day=0
    for i in range(1,nRounds+1):
        for j in range(nTeams//2+nTeams%2):
            newResult = Result()
            newResult.save()
            newGame = Game(result=newResult,team1=teams1[j],team2=teams2[j],tournament=tournament,gRound=i,slot=slots[day])
            newGame.save()
            games.append(newGame)
            day+=1

        teams1.insert(1,teams2[0])
        teams2.pop(0)
        teams2.append(teams1[-1])
        teams1.pop(-1)

    tournament.gRound = 1
    tournament.save()

    return HttpResponseRedirect(reverse('appEball:tournament_info', kwargs={'pk':pk,'gRound':tournament.gRound}))


def get_slots(startDate,nGames,tournamentSlots):
    
    slotsDays = list()
    game=0

    i=0    
    date = startDate
    prevDay= date.weekday()+1
    nextDay=tournamentSlots[0].weekDay
    while(True):
        if(nextDay-prevDay<0):
            sumDay=7-abs(nextDay-prevDay)
        else:
            sumDay=nextDay-prevDay

        date=date+datetime.timedelta(days=sumDay)

        hStart=tournamentSlots[i].start.hour
        mStart=tournamentSlots[i].start.minute

        hEnd=tournamentSlots[i].end.hour
        mEnd=tournamentSlots[i].end.minute

        while(hStart+1+(mStart+30)//60<hEnd or (hStart+1+(mStart+30)//60==hEnd and (mStart+30)%60<=mEnd)):
            newDate=datetime.datetime(day=date.day,month=date.month,year=date.year,hour=hStart,minute=mStart)
            daySlots=list(Slot.objects.filter(weekDay=newDate.weekday(),field=tournamentSlots[i].field,date=newDate))
            if(len(daySlots)==0):
                newSlot=Slot(weekDay=newDate.weekday(),date=newDate,field=tournamentSlots[i].field)
                newSlot.save()
                slotsDays.append(newSlot)
                game+=1
                if(game==nGames):
                    break
            hStart = hStart+1+(mStart+30)//60
            mStart = (mStart+30)%60
        
        if(game==nGames):
            break

        prevDay=nextDay
        i=(i+1)%len(tournamentSlots)
        nextDay = int(tournamentSlots[i].weekDay)

    for i in slotsDays:
        print(i.date.day,"/",i.date.month,"/",i.date.year,"-",i.date.hour,":",i.date.minute,"    ",i.field.name)

    return slotsDays

def change_round(request,pk,gRound,change):
    tournament=Tournament.objects.get(pk=pk)
    tournament.save()

    if(change=='plus'):
        gRound+=1
    else:
        gRound-=1
    
    return HttpResponseRedirect(reverse('appEball:tournament_info', kwargs={'pk':pk,'gRound':gRound}))



def my_calendar(request):
    games=list()
    teams=Player.objects.filter(user=request.user).values_list('team')
    allGames=(Game.objects.filter(team1__in=teams,slot__date__gte=timezone.now(),team2__isDayOff=False) | Game.objects.filter(team2__in=teams,slot__date__gte=timezone.now(),team1__isDayOff=False)).order_by('slot__date')
    for i in range(len(allGames)):
        if i%2==0:
            games.append([allGames[i],'row1'])
        else:
            games.append([allGames[i],'row2'])
    return render(request,'appEball/my_calendar.html',{'games':games})

class presencas(View):
    template_name= 'appEball/presencas.html'
   

    def get(self, request,pk):
        team = Team.objects.get(pk=pk)
        tournament=team.tournament
        jogadores=list(Player.objects.filter(team = team))
        players=list()
       

        for i in range(len(jogadores)):
            if(i%2==0):
                players.append(["row2",jogadores[i],team.played - jogadores[i].faltas])
            else:
                players.append(["row3",jogadores[i],team.played - jogadores[i].faltas])
           
        return render(request, self.template_name, {'team':team,'tournament':tournament,'players':players})

    def post(self, request,pk):
        if request.method=="POST":
            nomesMarked =  request.POST.getlist('checks')
            print(nomesMarked)
            team = Team.objects.get(pk=pk)
            jogadores=list(Player.objects.filter(team = pk))
            
            
            for jogador in jogadores:
                if jogador.user.firstName not in nomesMarked:
                    jogador.faltas+=1
                    jogador.isSub=True
                    jogador.isStarter=False
                    jogador.save()  
            for player in jogadores:
                if player.isSubbed:
                    player.subGames=-1
                    if player.subGames==0:
                        player.isSubbed=False
                        sub= Substitute.objects.filter(originalPlayer=player)
                        sub.delete()
                    player.save()

            return HttpResponseRedirect(reverse('appEball:tournaments'))


class game(View):
    template_name='appEball/game.html'

    def get(self,request,pk):
        game=Game.objects.get(pk=pk)
        jogadores1=list(Player.objects.filter(team=game.team1))
        jogadores2=list(Player.objects.filter(team=game.team2))
        players1=list()
        players2=list()
        isSt1=False
        isSt2=False

        isOver = game.slot.date +datetime.timedelta(hours=1,minutes=30) <= timezone.now()

        allPlayers1 = Player.objects.filter(team=game.team1).values_list('user',flat = True)
        allPlayers2 = Player.objects.filter(team=game.team2).values_list('user',flat = True)

        subs1 = Substitute.objects.filter(originalPlayer__in=allPlayers1)
        subs2 = Substitute.objects.filter(originalPlayer__in=allPlayers2)

        starterPlayers1Filter = list(Player.objects.filter(team=game.team1,isSubbed=False))
        starterPlayers2Filter = list(Player.objects.filter(team=game.team2,isSubbed=False))
        if(subs1.count()!=0):
            starterPlayers1Filter.append(subs1)
        if(subs2.count()!=0):
            starterPlayers2Filter.append(subs2)
        starterPlayers2Filter.append(subs2)
        print(starterPlayers2Filter)

        starterPlayers1 = list()
        starterPlayers2 = list()
        for i in range(len(starterPlayers1Filter)):
            if(i%2==0):
                if(isinstance(starterPlayers1Filter[i], Player)):
                    starterPlayers1.append(['row2',starterPlayers1Filter[i],True])
                else:
                    starterPlayers1.append(['row2',starterPlayers1Filter[i],False])

                if(isinstance(starterPlayers2Filter[i], Player)):
                    starterPlayers2.append(['row2',starterPlayers2Filter[i],True])
                else:
                    starterPlayers2.append(['row2',starterPlayers2Filter[i],False])
            else:
                if(isinstance(starterPlayers1Filter[i], Player)):
                    starterPlayers1.append(['row1',starterPlayers1Filter[i],True])
                else:
                    starterPlayers1.append(['row1',starterPlayers1Filter[i],False])

                if(isinstance(starterPlayers2Filter[i], Player)):
                    starterPlayers2.append(['row1',starterPlayers2Filter[i],True])
                else:
                    starterPlayers2.append(['row1',starterPlayers2Filter[i],False])

        return render(request, self.template_name,{'isOver':isOver,'game':game,'starterPlayers1':starterPlayers1,'starterPlayers2':starterPlayers2})

    def post(self, request, pk):
        form = GameForm(request.POST)
        if form.is_valid():
            game = Game.objects.get(pk=pk)
            if request.user == game.team1.captain:
                resultTeam1 = form.cleaned_data.get('team1Result')
                resultTeam2 = form.cleaned_data.get('team2Result')
                result = game.result
                result.goalsT1byC1 = resultTeam1
                result.goalsT2byC1 = resultTeam2
                result.save()
                if result.goalsT1byC2 != -1 and result.goalsT2byC2 != -1:
                    if result.goalsT1byC1 == result.goalsT1byC2 and result.goalsT2byC1 == result.goalsT2byC2:
                        result.goalsT1Final = result.goalsT1byC1
                        result.goalsT2Final = result.goalsT2byC1
                        self._registar_saldo(pk)
                    else:
                        n = Notification(text='The game between '+game.team1.name+' and '+game.team2.name+' does not have matching results! Better check that out!', title = 'Wrong results on '+game.tournament.name+'!', user=game.tournament.user)
                        n.save()
            elif request.user == game.team2.captain:
                resultTeam1 = form.cleaned_data.get('team1Result')
                resultTeam2 = form.cleaned_data.get('team2Result')
                result = game.result
                result.goalsT1byC2 = resultTeam1
                result.goalsT2byC2 = resultTeam2
                result.save()
                if result.goalsT1byC1 != -1 and result.goalsT2byC1 != -1:
                    if result.goalsT1byC1 == result.goalsT1byC2 and result.goalsT2byC1 == result.goalsT2byC2:
                        result.goalsT1Final = result.goalsT1byC2
                        result.goalsT2Final = result.goalsT2byC2
                        self._registar_saldo(pk)
                    else:
                        n = Notification(text='The game between '+game.team1.name+' and '+game.team2.name+' does not have matching results! Better check that out!', title = 'Wrong results on '+game.tournament.name+'!', user=game.tournament.user)
                        n.save()
            if request.user == game.tournament.user:
                resultTeam1 = form.cleaned_data.get('team1Result')
                resultTeam2 = form.cleaned_data.get('team2Result')
                result = game.result
                result.goalsT1Final = resultTeam1
                result.goalsT2Final = resultTeam2
                result.save()
                self._registar_saldo(pk)
            if result.goalsT1Final != -1 and result.goalsT2Final != -1:
                team1 = game.team1
                team2 = game.team2
                self._teamPoints(result, team1, team2)
            return HttpResponseRedirect(reverse('appEball:game', kwargs={'pk':pk}))

    def _registar_saldo(self, pk):
        game=Game.objects.get(pk=pk)
        jogadores1=list(Player.objects.filter(team=game.team1))
        jogadores2=list(Player.objects.filter(team=game.team2))

        for jogador1 in jogadores1:

            if jogador1.balance < game.slot.field.price:
                jogador1.isSub=True
                jogador1.faltas+=1
                jogador1.isStarter=False
                jogador1.save()
                for player in jogadores1:
                    if(player!=jogador1 and player.isSub==True and player.position==jogador1.position):
                        player.isSub=False
                        player.isStarter=True
                        player.save()

            elif jogador1.balance>game.slot.field.price:
                jogador1.balance-=game.slot.field.price
                if jogador1.balance<3:
                    jogador1.isSub=True
                    jogador1.isStarter=False
                    jogador1.save()
                    for player in jogadores1:
                        if(player!=jogador1 and player.isSub==True and player.position==jogador1.position):
                            player.isSub=False
                            player.isStarter=True
                            player.save()


        for jogador2 in jogadores2:

            if jogador2.balance < game.slot.field.price :
                jogador2.isSub=True
                jogador2.faltas+=1
                jogador2.isStarter=False
                jogador2.save()
                for player in jogadores2:
                    if(player!=jogador2 and player.isSub==True and player.position==jogador2.position):
                        player.isSub=False
                        player.isStarter=True
                        player.save()
            
            elif jogador2.balance>game.slot.field.price:
                jogador2.balance-=game.slot.field.price
                if jogador2.balance<3:
                    jogador2.isSub=True
                    jogador2.isStarter=False
                    jogador2.save()
                    for player in jogadores2:
                        if(player!=jogador2 and player.isSub==True and player.position==jogador2.position):
                            player.isSub=False
                            player.isStarter=True
                            player.save()

    def _teamPoints(self, result , team1, team2):
        if result.goalsT1Final > result.goalsT2Final:
            team1.points += 3
            team1.won += 1
            team2.lost += 1
        elif result.goalsT1Final == result.goalsT2Final:
            team1.points += 1
            team2.points += 1
            team1.drawn += 1
            team2.drawn += 1
        else:
            team2.points += 3
            team2.won += 1
            team1.lost += 1
        team1.goalsDif = (team1.goalsFor + result.goalsT1Final) - (team1.goalsAgainst + result.goalsT2Final) 
        team1.goalsFor += result.goalsT1Final
        team1.goalsAgainst += result.goalsT2Final
        team2.goalsDif = (team2.goalsFor + result.goalsT2Final) - (team2.goalsAgainst + result.goalsT1Final)
        team2.goalsFor += result.goalsT2Final
        team2.goalsAgainst += result.goalsT1Final
        team1.played += 1
        team2.played += 1
        team1.save()
        team2.save()

def next_matches(players):
    games=[]
    contador=0
    for player in players:
        games_t=list(Game.objects.filter(tournament=player.team.tournament))
        for game in games_t:
            if game.slot.date.date()>datetime.date.today():
                if game.team1==player.team or game.team2==player.team:
                    if contador%2==0:
                        games.append([game,'row1'])
                    else:
                        games.append([game,'row2'])
                    contador=contador+1
    sorted(games, key=lambda game: game[0].date)
    return games


def checkTeamName(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        teamName = data['teamName']
        tournament = data['tournamentName']
        try:
            teamObjs = Team.objects.filter(tournament=tournament)
            for team in teamObjs:
                if (team.name.lower() == teamName.lower()):
                    return JsonResponse({'is_taken':True})
            return JsonResponse({'is_taken':False})
        except IntegrityError as err:
            raise err
    else:
        raise Http404

def checkTournamentName(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        tournamentName = data['name']
        try:
            tournamentObj = Tournament.objects.all()
            for tournament in tournamentObj:
                if tournament.name.lower() == tournamentName.lower():
                    return JsonResponse({'is_taken':True})
            return JsonResponse({'is_taken': False})
        except IntegrityError as err:
            raise err
    else:
        raise Http404

def checkDates(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        startDate = data['startDate']
        if startDate!='':
            if (str(timezone.now()) > startDate):
                return JsonResponse({'is_valid':False})
            return JsonResponse({'is_valid':True})
        else:
            return JsonResponse({'is_valid':False})
    else:
        raise Http404

def checkRegister(request):
    data = json.loads(request.body)
    dataType = data['type']
    value = data['value']
    users = CustomUser.objects.all()
    if dataType == 'username':
        for user in users:
            if user.username.lower() == value.lower():
                return JsonResponse({'is_taken':dataType})
    elif dataType == 'email':
        for user in users:
            if user.email.lower() == value.lower():
                return JsonResponse({'is_taken':dataType})
    elif dataType == 'ccNumber':
        for user in users:
            if user.ccNumber == int(value):
                return JsonResponse({'is_taken':dataType})
    elif dataType == 'phoneNumber':
        for user in users:
            if user.phoneNumber == int(value):
                return JsonResponse({'is_taken':dataType})
    return JsonResponse({'is_taken':False})


class manage_team(View):
    template_name='appEball/manage_team.html'

    def get(self,request,pk):
        team=Team.objects.get(pk=pk)
        allplayers=list(Player.objects.filter(team=team))
        players=list()


        for i in range(len(allplayers)):
            if(i%2==0):
                players.append(["row2",allplayers[i],team.played - allplayers[i].faltas])
            else:
                players.append(["row1",allplayers[i],team.played - allplayers[i].faltas])

        return render(request, self.template_name,{'team':team,'players':players})

    def post(self,request,pk):
        team=Team.objects.get(pk=pk)
        if request.method=="POST":
            button_clicked1 = request.POST.get("submit_1")
            button_clicked2 = request.POST.get("submit_2")
            button_clicked3 = request.POST.get("submit_3")
            button_clicked4 = request.POST.get("submit_4")
            if(button_clicked1!=None):
                user=CustomUser.objects.get(pk=button_clicked1)
                team.captain=user
                team.save()
                print(team.captain)
                return HttpResponseRedirect(reverse('appEball:teams_list'))
            elif(button_clicked2!=None):
                player=Player.objects.get(pk=button_clicked2)
                player.isSub=False
                player.isStarter=True
                player.save()
            elif(button_clicked3!=None):
                player=Player.objects.get(pk=button_clicked3)
                player.isSub=True
                player.isStarter=False
                player.save()
            elif(button_clicked4!=None):
                Player.objects.get(pk=button_clicked4).delete()
            return HttpResponseRedirect(reverse('appEball:manage_team', kwargs={'pk':pk}))

def registar_saldo(request,pk):
    game=Game.objects.get(pk=pk)
    jogadores1=list(Player.objects.filter(team=game.team1))
    jogadores2=list(Player.objects.filter(team=game.team2))

    for jogador1 in jogadores1:
        if jogador1.balance < game.slot.field.price or jogador1.balance<3:
            jogador1.isSub=True
            jogador1.isStarter=False
            jogador1.save()
            for player in jogadores1:
                if(player!=jogador1 and player.isSub==True and player.position==jogador1.position):
                    player.isSub=False
                    player.isStarter=True
                    player.save()

    for jogador2 in jogadores2:
        if jogador2.balance < game.slot.field.price or jogador.balance<3:
            jogador2.isSub=True
            jogador2.isStarter=False
            jogador2.save()
            for player in jogadores2:
                if(player!=jogador2 and player.isSub==True and player.position==jogador2.position):
                    player.isSub=False
                    player.isStarter=True
                    player.save()

def sub_perm(request,teamId,subId):
    sub = Player.objects.get(team=teamId,pk=subId)
    sub.isSub = False
    sub.isStarter = True
    sub.save()
    user = Player.objects.get(team__pk=teamId,user=request.user)
    user.isSub = True
    user.isStarter = False
    user.save()
    return HttpResponseRedirect(reverse('appEball:team_info', kwargs={'teamId':teamId}))

def leave_team(request,teamId):
    player = Player.obejcts.get(team=teamId,user = request.user).delete()
    return HttpResponseRedirect(reverse('appEball:teams_list'))