from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from ..models import PortfolioItem
import requests, json
from .util import fget
from ..forms import SignUpForm, LoginForm

# Account management.
@csrf_exempt
def site_logout(request):
    logout(request)
    return redirect('/')

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
    return render(
        request=request,
        template_name='auth/login.html',
        context={'title': 'Login', 'form': form, 'portfolio': PortfolioItem.objects.all()}
    )

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
            login(request,newuser)
            webhook_url = "https://hooks.slack.com/services/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"  # Webhook URL
            text = {"text": newuser.first_name + " " + newuser.last_name + " just created an account!"}
            headers = {'Content-Type': 'application/json'}
            r = requests.post(webhook_url, data=json.dumps(text), headers=headers)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(
        request=request,
        template_name='auth/signup.html',
        context={'title': 'Sign Up', 'form':form, 'portfolio': PortfolioItem.objects.all()}
    )