# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import Exception

from django.db.models import Q, Count
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from random import *
# Create your views here.

class Break_Nested_Loop(Exception): pass
import datetime
import pytz
from django.core import serializers
from django.contrib.auth import update_session_auth_hash  # for enabling user to stay logged in after PW change
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.timezone import is_aware, is_naive
from django.views.generic import *
from django.contrib import messages
from .models import *
import re  # regex matching
# for generating/downloading grades
import csv
# import all of the JSON serializable classes
# separately define and import helper functions to improve modularity
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .customclasses import *
import os,sys
from .forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image



# DRY Utility Functions
def rp(request, data):
    return request.POST.get(data)
def isauth(request):
    return request.user.is_authenticated
def fget(form,string):
    return form.cleaned_data[string]
def ajax(request):
    return request.is_ajax()

# for ajax requests, returning JSON to JS
def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


@csrf_exempt
def index(request):
    context = {
        'portfolio': PortfolioItem.objects.all().order_by('-date'),
        'bio': MetaStuff.objects.all()[0].bio
        }
    if isauth(request):
        # post to slack with username
        webhook_url = "https://hooks.slack.com/services/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"  # Webhook URL
        text = {"text": request.user.first_name + " " + request.user.last_name + " is viewing your site!"}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(webhook_url, data=json.dumps(text), headers=headers)
        if request.user.is_superuser:
            template = loader.get_template('index_in_super.html')
        else:
            template = loader.get_template('index_in.html')
    else:
        template = loader.get_template('index.html')
    return HttpResponse(template.render(context,request))

# Account management.
@csrf_exempt
def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

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
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login/')
    form = LoginForm()
    template = loader.get_template('login.html')
    context = {'form': form, 'portfolio': PortfolioItem.objects.all()}
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
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()
    template = loader.get_template("signup.html")
    context = {'form':form, 'portfolio': PortfolioItem.objects.all()}
    return HttpResponse(template.render(context, request))






# Super mods.
@csrf_exempt
def upload(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST' and request.FILES['newfile']:
            # Save the regular image, but also save a 30% version to show in preview (smaller size = faster load)
            # Regular image
            myfile = request.FILES['newfile']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/drawings/", file_permissions_mode=0o655)
            filename = fs.save(myfile.name, myfile)
            print("Filename: ")
            print(filename)
            print("myfile.name")
            print(myfile.name)


            # Smaller Image
            try:
                img = Image.open(settings.MEDIA_ROOT+"/drawings/"+myfile.name)
                smallW = int(img.size[0] * .3)
                smallH = int(img.size[1] * .3)
                smallcopy = img.resize((smallW,smallH), Image.ANTIALIAS)
                smallcopy.save(settings.MEDIA_ROOT+'/copied_smaller_drawings/'+myfile.name)
                print(smallcopy)
            except Exception as e:
                print("Couldn't copy image.")
            date = rp(request,'date')
            # create a new object in DB for naming
            PortfolioItem(tag='Portrait',portrait_name=rp(request,"portraitname"),filename=myfile.name,date=date).save()
            return HttpResponseRedirect('/')
        template = loader.get_template('upload.html')
        context = {}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def delete(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            name = rp(request,'name') # filename;
            PortfolioItem.objects.filter(filename=name).delete()
            try:
                os.remove(settings.MEDIA_ROOT + "/drawings/" + name)
                # delete the smaller copy
                os.remove(settings.MEDIA_ROOT + "/copied_smaller_drawings/" + name)
            except:
                print("No image with that name.")
            return render_to_json_response({'msg':'success'})
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def update(request):
    print()


'''
def create_portfolio_items():
    imgnames = [l.strip() for l in open('sketchyactivity/imgnames.txt','r').readlines()]
    tags = ["Portrait"] * len(imgnames)
    portraitnames = [l.strip() for l in open('sketchyactivity/portraitnames.txt','r').readlines()]
    items = [PortfolioItem(tag=tags[i],portrait_name=portraitnames[i],filename=imgnames[i]).save() for i in range(35)]
'''


# SLACK
import requests
@csrf_exempt
def notify(request):
    webhook_url = "https://hooks.slack.com/services/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" #  Webhook URL
    text = {"text": "Someone is viewing your site!"}
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
        r = requests.post("http://sketchyactivity.com/messaging/"+uid+"/",data=payload)

    else:
        if request.user.is_authenticated: # redirect to /userid
            return HttpResponseRedirect("/messaging/" + str(request.user.id) + "/")
        else:
            return HttpResponseRedirect("/")




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
        return HttpResponseRedirect("/")


def update_profile(request):
    """ View for updating profile, starting for now just with bio """
    if request.method == "POST":
        bio = request.POST.get('bio','')
        ms = MetaStuff.objects.all()[0]
        ms.bio = bio
        ms.save()
        return HttpResponseRedirect("/")
    else:
        bio = MetaStuff.objects.all()[0].bio
        context = {'bio':bio}
        template = loader.get_template('update_profile.html')
        return HttpResponse(template.render(context,request))
