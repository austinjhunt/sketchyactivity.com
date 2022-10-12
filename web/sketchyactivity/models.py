
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import boto3
from botocore.client import Config
from django.conf import settings
import datetime
import logging 
logger = logging.getLogger('sketchyactivity')

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
    profile_image_filename = models.CharField(default='', max_length=100)
    profile_image_private_url = models.URLField(max_length=500, default="")
    website_title = models.CharField(max_length=128,default="")
    website_description = models.TextField(default="")
    website_keywords = models.TextField(default="")
    sale = models.BooleanField(default=False)
    sale_amount = models.FloatField(default=0)
    sale_start = models.DateField()
    sale_end = models.DateField()

    def sale_still_active(self):
        # current date is on or after sale_start and before or on sale_end
        today = datetime.datetime.today().date()
        return self.sale and today >= self.sale_start and today <= self.sale_end # sale active

    def get_sale_price(self, original_price):
        """ return the sale price of an item given original price """
        return round(original_price * (1 - self.sale_amount), 2)

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
    test = models.BooleanField(default=False) # indicate whether this was used for testing

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

## Receivers / listeners
@receiver(models.signals.post_delete, sender=Product)
def auto_delete_commission_reference_image_on_product_delete(sender, instance, **kwargs):
    """ When product is deleted, automatically use S3 client to delete S3 file corresponding 
    to product (the reference image) """ 
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2',
        config=Config(signature_version='s3v4'))
    try:
        s3_client.delete_object(
            Bucket='sketchyactivitys3', 
            Key=f'media/commission-reference-images/{instance.reference_image_filename}'
        )
    except Exception as e: 
        logger.error(str(e))

@receiver(models.signals.post_delete, sender=PortfolioItem)
def auto_delete_image_files_on_portfolio_item_delete(sender, instance, **kwargs):
    """ When product is deleted, automatically use S3 client to delete S3 file corresponding 
    to product (the reference image) """ 
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2',
        config=Config(signature_version='s3v4'))
    try:
        s3_client.delete_object(
            Bucket='sketchyactivitys3', 
            Key=f'media/drawings/{instance.filename}'
        )
    except Exception as e: 
        logger.error(str(e))
    try:
        s3_client.delete_object(
            Bucket='sketchyactivitys3', 
            Key=f'media/copied_smaller_drawings/{instance.filename}'
        )
    except Exception as e: 
        logger.error(str(e))