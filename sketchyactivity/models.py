
from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class PortfolioItem(models.Model):
    tag = models.CharField(default='',max_length=100)
    filename = models.CharField(default='',max_length=100)
    portrait_name = models.CharField(default='',max_length=100)
    date = models.DateField(null=True)

class MetaStuff(models.Model):
    bio = models.TextField(default='')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
