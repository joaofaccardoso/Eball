from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

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


dayChoice=(('Sun','Sun'),('Mon','Mon'),('Tue','Tue'),('Wed','Wed'),('Thu','Thu'),('Fri','Fri'),('Sat','Sat'))
class Tournament(models.Model):
    name=models.CharField(max_length=100, blank=False, unique=True)
    maxTeams = models.IntegerField(unique=False, blank=False)
    beginDate=models.DateField(('Tournament Start Date'),default=datetime.date.today)
    endDate=models.DateField(('Tournament End Date'),default=datetime.date.today)
    gameDays=MultiSelectField(choices=dayChoice,default= None )
    user = models.ForeignKey(CustomUser,default=None,on_delete=models.SET_DEFAULT)

    REQUIRED_FIELDS = ['name','maxTeams','beginDate','endDate','user']

    class Meta:
        db_table = 'Tournament'
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'

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

    REQUIRED_FIELDS = ['name','tactic','tournament','captain']

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
    team=models.ForeignKey(Team, default = None, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Player'
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        ordering = ['team', '-isStarter', '-position']
    
    def __str__(self):
        return self.user.username+" || "+self.team.name+' || '+self.position
