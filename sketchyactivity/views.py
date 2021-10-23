# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from random import *
from django.contrib.auth.models import User
from django.template import loader
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.views import View
import boto3
from botocore.client import Config
from django.core.cache import cache
from .models import *
from .customclasses import *
from .forms import *
from .util import *

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2',
    config=Config(signature_version='s3v4'))

def get_bio():
    return MetaStuff.objects.all()[0].bio

def get_bio_split(bio=None):
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

@csrf_exempt
def index(request):
    bio = get_bio()
    bio_split = get_bio_split(bio=bio)[0]

    portfolio = PortfolioItem.objects.all().order_by('-date')
    # update private urls if they need to be updated
    if not cache.get('updated_private_video_url'):
        private_video_url = update_private_video_url(s3_client)
        cache.set('updated_private_video_url', private_video_url, timeout=302400)# half the max expiration time of the private urls for the media files in s3.
    if not cache.get('updated_private_urls'):
        print("Updating private urls for portfolio...")
        update_private_urls_full_portfolio(portfolio,s3_client)
        print("Setting cache.updated_private_urls ")
        cache.set('updated_private_urls', 'is_updated',timeout=302400) # half the max expiration time of the private urls for the media files in s3.
    else:
        print("Cache updated_private_urls is set already")
    context = {
        'featured': portfolio[0],
        'title': 'Austin Hunt Portraiture',
        'portfolio': portfolio,
        'bio_1': bio_split[0],
        'bio_2': bio_split[-1],
        'bio': bio,
        'private_video_url': cache.get('updated_private_video_url')
        }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context,request))

# Account management.
@csrf_exempt
def site_logout(request):
    logout(request)
    return redirect('/')

from django.contrib.auth import authenticate
@csrf_exempt
def site_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = fget(form, "email")
            password = fget(form, "password")
            user = authenticate(username=email, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request,user)
                return redirect('/')
            else:
                return redirect('/login')
    form = LoginForm()
    template = loader.get_template('auth/login.html')
    context = {'title': 'Login', 'form': form, 'portfolio': PortfolioItem.objects.all()}
    return HttpResponse(template.render(context,request))
    # No backend authenticated the credentials

@csrf_exempt
def site_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = fget(form,"first_name")
            last_name = fget(form,"last_name")
            email = fget(form, "email")
            password = fget(form, "password")
            phone = fget(form, "phone")
            newuser = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                     username=email, password=password)
            UserProfile(phone=phone, user=newuser).save()
            login(request,newuser)
            webhook_url = "https://hooks.slack.com/services/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"  # Webhook URL
            text = {"text": newuser.first_name + " " + newuser.last_name + " just created an account!"}
            headers = {'Content-Type': 'application/json'}
            r = requests.post(webhook_url, data=json.dumps(text), headers=headers)
            return redirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()
    template = loader.get_template("auth/signup.html")
    context = {'title': 'Sign Up', 'form':form, 'portfolio': PortfolioItem.objects.all()}
    return HttpResponse(template.render(context, request))

def media(request, path, filename):
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    return (
        s3.get_object(
            Bucket='sketchyactivitys3',
            Key=f'{path}/{filename}'
        )
    )

def s3callback(request):
    if request.method == "POST":
        print("post request from S3")
        print(request)
        print(request.POST)
    elif request.method == "GET":
        print("get request from S3")
        print(request)
        print(request.GET)
    return JsonResponse({'response':'thanks for calling back'})


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 3 for x in image.size))
        image.save(resized_path)

# Super mods.
@csrf_exempt
def upload(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST' and request.FILES['newfile']:
            """ Have inmemoryuploadedfile. That's what uploadprivate expects as file arg. need to
            1. save original with upload private in the 'drawings' """
            # Save the regular image, but also save a 30% version to show in preview (smaller size = faster load)
            # Regular image

            myfile = request.FILES['newfile']
            fs = FileSystemStorage(location='', file_permissions_mode=0o655)
            filename = fs.save(myfile.name, myfile)
            response1 = s3_client.upload_file(
                filename,
                'sketchyactivitys3',
                f'media/drawings/{myfile.name}',
                ExtraArgs={
                    'ACL':'private'
                }
            )
            resize_path = f'/tmp/{filename}'
            resize_image(filename,  resize_path)
            response2 = s3_client.upload_file(
                resize_path,
                'sketchyactivitys3',
                f'media/copied_smaller_drawings/{myfile.name}',
                ExtraArgs={'ACL':'private'}
                )
            os.remove(filename)
            # Initialize private urls to empty strings
            s3_drawing_private_url = ""
            s3_copied_smaller_drawing_private_url = ""

            tag = rp(request, 'tag')
            if not tag:
                tag = 'Portrait'

            date = rp(request,'date')
            # create a new object in DB for naming
            new_item = PortfolioItem(
                tag=tag,
                portrait_name=rp(request,"portraitname"),
                filename=myfile.name,
                date=date,
                s3_drawing_private_url=s3_drawing_private_url,
                s3_copied_smaller_drawing_private_url=s3_copied_smaller_drawing_private_url)
            new_item.save()

            update_private_url_single(new_item, s3_client)

            return redirect('/')
        template = loader.get_template('super/upload.html')
        context = {'title': 'Add Content'}
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

@csrf_exempt
def delete(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            name = rp(request,'name') # filename;
            PortfolioItem.objects.filter(filename=name).delete()
            delete_session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name='us-east-2').resource('s3')
            orig = delete_session.Object(
                'sketchyactivitys3', # bucket
                f'media/drawings/{name}' # original drawing file
                )
            orig.delete()

            thumb = delete_session.Object(
                'sketchyactivitys3', # bucket
                f'media/copied_smaller_drawings/drawings/{name}' # original drawing file
                )
            thumb.delete()
            return render_to_json_response({'msg':'success'})
    else:
        return redirect('/')


# SLACK
import requests
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



# Have to use long polling for pushing API responses from Slack to front end without front end triggering updates.
# use responses dictionary with key,val = client, last response from me
# whenever new response for given client pushed to front end (check every 10 secs), make value for key null
responses = {}


@csrf_exempt
def slack_msging_endpoint(request):
    # get the user id.
    if request.method == "POST" : # api call from slack
        """
        request.POST = {
            'token': ['GniqX5w41BdkPoaFbefNV1wE'],
            'team_id': ['TN3C0CHBN'],
            'team_domain': ['sketchyactivity'],
            'channel_id': ['CMU91TEV8'],
            'channel_name': ['website-messaging'],
            'user_id': ['UMSC0SARZ'],
            'user_name': ['huntaj'],
            'command': ['/snd'],
            'text': ['1 hi'],
            'response_url': ['https://hooks.slack.com/commands/TN3C0CHBN/749204736337/U08DRq3LtUvZBdoWtw9T09WN'],
            'trigger_id': ['744145688451.751408425396.3a96fb8b035cc516c3cf8977580417e7']
        }
        """
        data = dict(request.POST)
        print(data)
        text = data['text'][0]
        print("Text:",text)
        uid = text.split()[0]
        message = text[text.index(" ")+1:]
        print("Sending message: ", message)
        # Post to /messaging/uid with message.
        payload = {'text': message, 'slack': ''}
        r = requests.post(f"http://sketchyactivity.com/messaging/{uid}",data=payload)

    else:
        if request.user.is_authenticated: # redirect to /userid
            return redirect(f"/messaging/{request.user.id}")
        else:
            return redirect("/")




@csrf_exempt
def messaging(request,userid):
    if request.user.is_authenticated or 'slack' in request.POST:
        if request.method == "POST":
            # if client sending a message out
            try:

                sender = request.user.first_name + " " + request.user.last_name
                message = rp(request, "message") # will fail in post from slack since posting from slack does not offer this dictionary key
                responses[str(userid)] = ""
                # add this user's id as a key to responses dictionary if not already there.
                messaging_endpoint = "https://hooks.slack.com/services/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"
                payload = {
                    "text": message,
                    "attachments": [
                        {
                            "text": "*From " + sender + " with UID " + str(request.user.id) + "*",
                            "fallback": "You are unable to respond. ",
                            "callback_id": "respond_to_msg",
                            "color": "#3AA3E3",
                            "attachment_type": "default",

                        }
                    ]
                }
                payload = json.dumps(payload)

                headers = {'Content-Type': 'application/json'}

                r = requests.post(messaging_endpoint, data=payload, headers=headers)
                # send user initials back.
                inits = request.user.first_name[0] + request.user.last_name[0]
                data = {'inits': inits}
                return render_to_json_response(data)

            except: # must be a post response from slack (that is, slack -> django endpoint -> post to this URL after extracting UID and msg

                print("Setting new message response for this user!")
                data = dict(request.POST)
                print("data: ")
                print(data)
                message = data['text']
                print("Message")
                # make this the most recent response to this user in responses dictionary.
                responses[str(userid)] = message

        if request.is_ajax() : # long polling for backend slack responses
            if str(userid) not in responses:
                print("user id not in responses. emptying.")
                responses[str(userid)] = ""
            message = responses[str(userid)]
            print("Message:",message)
            responses[str(userid)] = ""
            data = {'message': message}
            return render_to_json_response(data)


        template = loader.get_template('messaging.html')
        context = {}
        return HttpResponse(template.render(context,request))
    else: # not authenticated
        return redirect("/")


def update_profile(request):
    """ View for updating profile, starting for now just with bio """
    if request.method == "POST":
        bio = request.POST.get('bio','')
        website_title = request.POST.get('website_title','')
        website_description = request.POST.get('website_description','')
        website_keywords = request.POST.get('website_keywords','')

        ms = MetaStuff.objects.all()[0]
        ms.website_title = website_title
        ms.website_description = website_description
        ms.website_keywords = website_keywords
        ms.bio = bio
        ms.save()
        return redirect("/")
    else:
        bio = MetaStuff.objects.all()[0].bio
        context = {'bio':bio, 'title': 'Update Website'}
        template = loader.get_template('super/update_profile.html')
        return HttpResponse(template.render(context,request))



class CommissionsView(View):
    def get(self, request):
        return render(
            request,
            'commissions.html',
            context={
                'title': 'Austin Hunt Portraiture Commissions',
                'prices': Price.objects.all()
            }
        )

class PortfolioItemEdit(UpdateView):
    model = PortfolioItem
    template_name = 'super/portfolio_item_edit.html'
    fields = ['tag', 'portrait_name', 'date']
    success_url = '/'

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class PortfolioManage(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'super/manage_portfolio.html'
    def get(self,request):
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'portfolio': PortfolioItem.objects.all()
            }
        )
    def test_func(self):
        return self.request.user.is_superuser
