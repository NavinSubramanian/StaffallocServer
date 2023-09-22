from django.db import models

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