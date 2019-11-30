from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator 

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, blank=False)
    firstName = models.CharField(max_length=100, blank=False)
    lastName = models.CharField(max_length=100, blank=False)
    ccNumber = models.IntegerField(unique=True, blank=False)
    phoneNumber = models.IntegerField(unique=True, blank=False)
    profileImg = models.ImageField(upload_to="appEball/", default = "/../media/appEball/photo1.png")
    isAccepted = models.BooleanField(default=False)
    isTournamentManager = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstName', 'lastName', 'ccNumber', 'phoneNumber']

    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ["username"]

    def __str__(self):
        return self.username


class Tactic(models.Model):
    name = models.CharField(max_length=10, unique=True, blank=False)
    nGK = models.IntegerField(default=2, blank=False)
    nDF = models.IntegerField(default=5, blank=False)
    nMF = models.IntegerField(default=4, blank=False)
    nFW = models.IntegerField(default=3, blank=False)
    nST = models.IntegerField(default=2, blank=False)
    #imgTactic = models.ImageField(upload_to="images")      para adicionar mais tarde

    class Meta:
        db_table = 'Tactic'
        verbose_name = 'Tactic'
        verbose_name_plural = 'Tactics'

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name=models.CharField(max_length=100, blank=False, unique=True)
    maxTeams = models.IntegerField(unique=False, blank=False)
    beginDate=models.DateField(('Tournament Start Date'),default=datetime.date.today)
    user = models.ForeignKey(CustomUser,default=None,on_delete=models.SET_DEFAULT)
    gRound=models.IntegerField(unique=False,default=0)

    REQUIRED_FIELDS = ['name','maxTeams','beginDate','endDate','user']

    class Meta:
        db_table = 'Tournament'
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'

    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    price=models.FloatField(default=3)

    class Meta:
        db_table = 'Field'
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'

    def __str__(self):
        return self.name

class Team(models.Model):
    name=models.CharField(max_length=100, blank=False)
    availGK = models.IntegerField(default=2)
    availDF = models.IntegerField(default=5)
    availMF = models.IntegerField(default=4)
    availFW = models.IntegerField(default=3)
    availST = models.IntegerField(default=2)
    tactic = models.ForeignKey(Tactic, default=None, on_delete=models.SET_DEFAULT)
    tournament=models.ForeignKey(Tournament,default = None,on_delete=models.CASCADE)
    captain = models.ForeignKey(CustomUser,default=None,on_delete=models.SET_DEFAULT)
    isDayOff = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    goalsFor = models.IntegerField(default=0)
    goalsAgainst = models.IntegerField(default=0)
    goalsDif = models.IntegerField(default=0)
    played = models.IntegerField(default=0)


    REQUIRED_FIELDS = ['name','tactic','tournament']

    class Meta:
        db_table = 'Team'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['name']

    def __str__(self):
        return self.name

class Notification(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    title = models.TextField(blank = False, default="")
    text = models.TextField(blank = False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    isSeen = models.BooleanField(default = False)


class Player(models.Model):
    position = models.CharField(max_length=100,default= None)
    balance = models.IntegerField(unique=False, default= 0)
    nrGoals = models.IntegerField(unique=False, default= 0)
    isStarter = models.BooleanField(default=False)
    isSub = models.BooleanField(default=False)
    isSubbed=models.BooleanField(default=False)
    subGames=models.IntegerField(unique=False, default= 0)
    team=models.ForeignKey(Team, default = None, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    faltas=models.IntegerField(default=0)

    class Meta:
        db_table = 'Player'
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        ordering = ['team', '-isStarter', '-position']
    
    def __str__(self):
        return self.user.username+" || "+self.team.name+' || '+self.position

    
class Reserve(models.Model):
    tournament=models.ForeignKey(Tournament,on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    
    class Meta:
        db_table = 'Reserve'
        verbose_name = 'Reserve'
        verbose_name_plural = 'Reserves'


    


        
class Slot(models.Model):
    week=((0,'Sun'),(1,'Mon'),(2,'Tue'),(3,'Wed'),(4,'Thu'),(5,'Fri'),(6,'Sat'))
    
    field = models.ForeignKey(Field,default=None,on_delete=models.CASCADE)
    weekDay = models.IntegerField(choices=week,default=0,validators=[MinValueValidator(0), MaxValueValidator(6)])
    date = models.DateTimeField(default=None, null=True)
    start = models.TimeField(default=None, null=True)
    end = models.TimeField(default=None, null=True)
    tournament = models.ForeignKey(Tournament, default=None, null=True,on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['field','weekDay','end','start']

    class Meta:
        db_table = 'Slot'
        verbose_name = 'Slot'
        verbose_name_plural = 'Slots'
    
    def __str__(self):
        return str(self.weekDay) + ", " + str(self.start) + " - " + str(self.end)

class Result(models.Model):
    goalsT1byC1 = models.IntegerField(default=-1)
    goalsT2byC1 = models.IntegerField(default=-1)
    goalsT1byC2 = models.IntegerField(default=-1)
    goalsT2byC2 = models.IntegerField(default=-1)
    goalsT1Final = models.IntegerField(default=-1)
    goalsT2Final = models.IntegerField(default=-1)

class Game(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, default=None)
    team1 = models.ForeignKey(Team,on_delete=models.CASCADE,default = None,related_name='team1')
    team2 = models.ForeignKey(Team,on_delete=models.CASCADE,default = None,related_name='team2')
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,default=None)
    gRound = models.IntegerField(default = 0)
    goalsT1_byT1 = models.IntegerField(default=0)
    goalsT1_byT2 = models.IntegerField(default=0)
    goalsT1_byManager = models.IntegerField(default=0)
    slot = models.ForeignKey(Slot,default=None,on_delete=models.SET_DEFAULT)

    class Meta:
        db_table = 'Game'
        verbose_name = 'Game'   
        verbose_name_plural = 'Games'
    
    def __str__(self):
        return self.team1.name + " vs " + self.team2.name

class TournamentDays(models.Model):

    name=models.CharField(max_length=100, blank=False, unique=True)
    maxTeams = models.IntegerField(unique=False, blank=False)
    beginDate=models.DateField(('Tournament Start Date'),default=datetime.date.today)

    REQUIRED_FIELDS = ['name','maxTeams','beginDate','user']



class Substitute(models.Model):
    reserveSub=models.ForeignKey(Reserve,null=True, on_delete=models.CASCADE,related_name='reserveSub')
    playerSub=models.ForeignKey(Player,null=True, on_delete=models.CASCADE)
    originalPlayer=models.ForeignKey(Player,null=True, on_delete=models.CASCADE,related_name='originalPlayer')
    hasAccepted= models.BooleanField(default=True) #tem de estar a false mas é so para teste
    isActive=models.BooleanField(default=True)
    nrGoals = models.IntegerField(default=0)


    class Meta:
        db_table = 'Substitute'
        verbose_name = 'Substitute'
        verbose_name_plural = 'Substitutes'
         
