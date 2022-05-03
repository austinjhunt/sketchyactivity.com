
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    website_title = models.CharField(max_length=128,default="")
    website_description = models.TextField(default="")
    website_keywords = models.TextField(default="")
    sale = models.BooleanField(default=False)
    sale_amount = models.FloatField(default=0)
    sale_start = models.DateField()
    sale_end = models.DateField()

class Product(models.Model):
    """ Products that a user adds to their cart """
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    type = models.TextField()
    price = models.FloatField()
    reference_image_filename = models.CharField(default='', max_length=100)
    s3_reference_image_url = models.URLField(max_length=500,default="")
    class CommissionStatus(models.TextChoices):
        NOT_STARTED = 'NS', _('Not Started Yet')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETE = 'CMPLT', _('Complete')
    status = models.CharField(
        max_length=10,
        choices=CommissionStatus.choices,
        default=CommissionStatus.NOT_STARTED
    )
    completion_date = models.DateField(null=True,blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    cart = models.ManyToManyField(Product)
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        print(instance.__dict__)
        instance.userprofile.save()

class Purchase(models.Model):
    """ keep record of purchase """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_created=True) # save as now when purchase created
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
