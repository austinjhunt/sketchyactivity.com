
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

from django.contrib.auth.models import User
from decimal import Decimal
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
    website_title = models.CharField(max_length=128,default="")
    website_description = models.TextField(default="")
    website_keywords = models.TextField(default="")
    sale = models.BooleanField(default=False)
    sale_amount = models.FloatField(default=0)
    sale_start = models.DateField()
    sale_end = models.DateField()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
class Price(models.Model):
    amount = models.FloatField(default=0)
    description = models.TextField(default="")

    size = models.CharField(max_length=100, default='8.5x12in')
    num_subjects = models.IntegerField(default=1)
    class DrawingStyle(models.TextChoices):
        TRADITIONAL = 'TR', _('Traditional')
        DIGITAL = 'DI', _('Digital')

    style = models.CharField(
        max_length=2,
        choices=DrawingStyle.choices,
        default=DrawingStyle.TRADITIONAL
    )
