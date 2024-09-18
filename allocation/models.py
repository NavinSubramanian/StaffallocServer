from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    name=models.CharField(max_length=2080)
    department=models.CharField(max_length=2080)
    email=models.CharField(max_length=2080)
    password=models.CharField(max_length=2080)

class Staff(models.Model):
    name=models.CharField(max_length=2080)
    designation=models.CharField(max_length=2080)
    department=models.CharField(max_length=2080)
    gender=models.CharField(max_length=2080)
    subcode=models.CharField(max_length=2080)

class Rooms(models.Model):
    roomno=models.CharField(max_length=20)

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.username