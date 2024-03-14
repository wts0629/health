from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    sex=models.IntegerField(default=0)
    headicon=models.CharField(max_length=60,default='')

class recordinfo(models.Model):
    rid=models.AutoField(primary_key=True)
    userid=models.IntegerField()
    starttime=models.CharField(max_length=300,null=True)
    endtime=models.CharField(max_length=300,null=True)
    hours=models.DecimalField(max_digits=10, decimal_places=2)
