from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, blank=False)
    firstName = models.CharField(max_length=100, blank=False)
    lastName = models.CharField(max_length=100, blank=False)
    ccNumber = models.IntegerField(unique=True, blank=False)
    phoneNumber = models.IntegerField(unique=True, blank=False)
    profileImg = models.ImageField(upload_to="images")
    isAccepted = models.BooleanField(default=False)
    isPageAdmin = models.BooleanField(default=False)
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


    
class Tournament(models.Model):

        name=models.CharField(max_length=100, blank=False)
        maxTeams = models.IntegerField(unique=False, blank=False)
        beginDate=models.DateField(('Tournament Start Date'),default=datetime.date.today)
        endDate=models.DateField(('Tournament End Date'),default=datetime.date.today)

        REQUIRED_FIELDS = ['name','maxTeams','beginDate','endDate']

        class Meta:
            db_table = 'Tournament'
            verbose_name = 'Tournament'
            verbose_name_plural = 'Tournaments'

        def __str__(self):
            return self.name

