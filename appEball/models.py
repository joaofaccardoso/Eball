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
    profileImg = models.ImageField(upload_to="images")
    isAccepted = models.BooleanField(default=False)
    isTournamentManager = models.BooleanField(default=False)
    isCaptain = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstName', 'lastName', 'ccNumber', 'phoneNumber']

    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ["-username"]

    def __str__(self):
        return self.username



dayChoice=(('Sun','Sun'),('Mon','Mon'),('Tue','Tue'),('Wed','Wed'),('Thu','Thu'),('Fri','Fri'),('Sat','Sat'))
class Tournament(models.Model):

        name=models.CharField(max_length=100, blank=False)
        maxTeams = models.IntegerField(unique=False, blank=False)
        beginDate=models.DateField(('Tournament Start Date'),default=datetime.date.today)
        endDate=models.DateField(('Tournament End Date'),default=datetime.date.today)
        gameDays=MultiSelectField(choices=dayChoice,default= None )

        REQUIRED_FIELDS = ['name','maxTeams','beginDate','endDate']

        class Meta:
            db_table = 'Tournament'
            verbose_name = 'Tournament'
            verbose_name_plural = 'Tournaments'

        def __str__(self):
            return self.name

tacticChoice=(('4-3-3','4-3-3'),('4-4-2','4-4-2'),('4-2-3-1','4-2-3-1'),('4-1-2-1-2','4-1-2-1-2'))




class Notification(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    title = models.TextField(blank = False, default="")
    text = models.TextField(blank = False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    isSeen = models.BooleanField(default = False)



class Tactic(models.Model):
    n_def=models.IntegerField(unique=False, default= 0)
    n_atac=models.IntegerField(unique=False, default= 0)
    n_cent=models.IntegerField(unique=False, default= 0)
    scorer=models.BooleanField(default=False)



positionChoice=(('Goalkeeper','Goalkeeper'),('Defender','Defender'),('Mildfielder','Mildfielder'),('Foward','Foward'),('Striker','Striker'))
class Player(models.Model):
    posicao = models.CharField(choices=positionChoice,max_length=100,default= None)
    saldo= models.IntegerField(unique=False, default= 0)
    nrGolos= models.IntegerField(unique=False, default= 0)
    isTitular = models.BooleanField(default=False)
    isReserva = models.BooleanField(default=False)
    isSub = models.BooleanField(default=False)
    #equipa=models.ForeignKey(Team, default = None, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, default = None, on_delete=models.CASCADE)


    class Meta:
            db_table = 'Player'
            verbose_name = 'Player'
            verbose_name_plural = 'Players'

    def __str__(self):
        return self.name





class Team(models.Model):

        name=models.CharField(max_length=100, blank=False)
        members=models.ManyToManyField(Player)
        tactic = models.ForeignKey(Tactic, on_delete=models.CASCADE)
        REQUIRED_FIELDS = ['name','tactic']

        class Meta:
            db_table = 'Team'
            verbose_name = 'Team'
            verbose_name_plural = 'Teams'

        def __str__(self):
            return self.name