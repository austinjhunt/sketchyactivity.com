
from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class PortfolioItem(models.Model):
    tag = models.CharField(default='',max_length=100)
    filename = models.CharField(default='',max_length=100)
    portrait_name = models.CharField(default='',max_length=100)
    date = models.DateField(null=True)
    # Each item stored twice. One big, one small copy for preview. Need private url for each.
    s3_drawing_private_url = models.URLField(max_length=500,default="")
    s3_copied_smaller_drawing_private_url = models.URLField(max_length=500,default="")

class MetaStuff(models.Model):
    bio = models.TextField(default='')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

class Price(models.Model):
    amount = models.FloatField(default=0)
    description = models.TextField(default="")