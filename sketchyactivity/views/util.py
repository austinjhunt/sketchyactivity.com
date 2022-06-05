from ..models import *
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import boto3
from PIL import Image
import requests
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger('sketchyactivity')
MAX_EXPIRATION_ONE_WEEK_SECS = 604800


def get_bio():
    """ Get bio from meta stuff model """
    return MetaStuff.objects.all()[0].bio

def get_bio_split(bio=None):
    """ split bio """
    bio_split = bio.split('\n\n')
    if len(bio_split) < 2:
        bio_split = bio.split("\r\r")
        if len(bio_split) < 2:
            bio_split = bio.split("\r\n\r\n")
    return bio_split,bio

def portfolio_item(request, id):
    item = PortfolioItem.objects.get(id=id)
    return render(
        request,
        template_name='pitem.html',
        context={
            'title': f'Austin Hunt Portraiture - {item.portrait_name}',
            'preview_image': item.s3_drawing_private_url,
            'item': item
        }
    )

# DRY Utility Functions
def rp(request, data):
    return request.POST.get(data)
def isauth(request):
    return request.user.is_authenticated
def fget(form,string):
    return form.cleaned_data[string]
def ajax(request):
    return request.is_ajax()

def get_total_price_from_cart(cart):
    """ return the total price of all the items in a user profile's cart
    attribute (many to many relation with Product model).
    truncate with int. stripe expects integer for amount argument.

    Total is then multiplied by 100 because Stripe epxects amounts to be provided in currency's
    smallest unit (cents).
    https://stripe.com/docs/currencies#zero-decimal
    Example. To charge 10USD, provide an amount value of 1000 (1000 cents).
    """
    from django.db.models import Sum
    price_sum = cart.aggregate(Sum('price'))['price__sum']
    if price_sum is not None:
        total = int(cart.aggregate(Sum('price'))['price__sum']) * 100
    else:
        total = 0
    return total

def render_to_json_response(context, **response_kwargs):
    """ for ajax requests, returning JSON to JS """
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)

def update_private_url_single(item,s3_client):
    item.s3_drawing_private_url = s3_client.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': 'sketchyactivitys3',
                                                    'Key': f'media/drawings/{item.filename}'},
                                                ExpiresIn=MAX_EXPIRATION_ONE_WEEK_SECS)

    item.s3_copied_smaller_drawing_private_url = s3_client.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': 'sketchyactivitys3',
                                                    'Key': f'media/copied_smaller_drawings/{item.filename}'},
                                                ExpiresIn=MAX_EXPIRATION_ONE_WEEK_SECS)
    item.save()

def update_private_url_profile_image(item,s3_client):
    """ Update the private URL for the profile image stored in media/admin/."""
    item.profile_image_private_url = s3_client.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': 'sketchyactivitys3',
                                                    'Key': f'media/admin/{item.profile_image_filename}'},
                                                ExpiresIn=MAX_EXPIRATION_ONE_WEEK_SECS) 
    item.save()

def update_private_url_product_reference_image(item, s3_client):
    """ Update the private reference image URL for single Product """
    logger.info('getting reference image s3 private url')
    item.s3_reference_image_url = s3_client.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': 'sketchyactivitys3',
                                                    'Key': f'media/commission-reference-images/{item.reference_image_filename}'},
                                                ExpiresIn=MAX_EXPIRATION_ONE_WEEK_SECS)
    logger.info(f'item.s3_reference_image_url = {item.s3_reference_image_url} ')
    item.save()

def update_private_video_url(s3_client):
    return s3_client.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': 'sketchyactivitys3',
                                                    'Key': f'media/videos/mischvid.mp4'},
                                                ExpiresIn=MAX_EXPIRATION_ONE_WEEK_SECS)

def update_private_urls_full_portfolio(portfolio=None,s3_client=None):
    if portfolio:
        for p in portfolio:
            update_private_url_single(p, s3_client)

def media(request, path, filename):
    """ return s3 media object """
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    return (
        s3.get_object(
            Bucket='sketchyactivitys3',
            Key=f'{path}/{filename}'
        )
    )

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 3 for x in image.size))
        image.save(resized_path)

@csrf_exempt
def notify(request):
    """ Send a notification that someone is viewing site to Slack channel. If auth, include username. else, Someone."""
    if not isauth(request):
        webhook_url = "https://hooks.slack.com/services/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" #  Webhook URL
        text = {"text": "Someone is viewing your site!"}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(webhook_url, data=json.dumps(text), headers=headers)
    elif isauth(request):
        # post to slack with username
        webhook_url = "https://hooks.slack.com/services/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"  # Webhook URL
        text = {"text": request.user.first_name + " " + request.user.last_name + " is viewing your site!"}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(webhook_url, data=json.dumps(text), headers=headers)
    return render_to_json_response({})

