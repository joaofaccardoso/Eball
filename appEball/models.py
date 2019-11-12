from django.db import models

class User(models.Model):
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=30)
    email=models.CharField(max_length=100)
    ccNumber=models.IntegerField()
    phoneNumber=models.IntegerField()

    