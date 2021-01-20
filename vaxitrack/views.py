from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django_q import tasks as qtasks
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Centre, User
from .forms import RegForm, LogForm, UserForm

import numpy as np
from random import randint

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def userpage(request):
    # return HttpResponse('Hello from Python!')
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        name = str(form['name'].value())
        age = str(form['age'].value())
        pc = str(form['postcode'].value())
        email = str(form['email'].value())
        body = "Hi " + name + ". We will let you know if a vaccine is available today within 10 miles of " + pc + ". Thanks, VaxiTrack"
        send_mail("VaxiTrack: Logged",body,"vaxitrack@gmail.com",[email],fail_silently=False)
        form = UserForm()

    return render(request, "vaxpage.html", {'form': form})


    return render(request, "userpage.html", {'form': form})

def vaxpage(request):
    # return HttpResponse('Hello from Python!')
    if request.method == 'GET':
        form = LogForm()
    else:
        form = LogForm(request.POST)
        doses_available = str(form['doses_available'].value())
        type = str(form['type'].value())
        start_time = str(form['start_time'].value())
        body = "You have logged " + doses_available + " doses of " + type + " available at " + start_time + " today"
        send_mail("VaxiTrack: Vaccines Logged",body,"vaxitrack@gmail.com",['ajbarker93@gmail.com'],fail_silently=False)
        form = LogForm()

    return render(request, "vaxpage.html", {'form': form})

def regpage(request):

    if request.method == 'GET':
        form = RegForm()
    else:
        form = RegForm(request.POST)
        id = str(randint(1e6,1e7-1)) # save this to our db append
        cname = str(form['cname'].value())
        email = str(form['email'].value())
        body = "Your VaxiTrack Centre ID for " + cname + " is: " +  id
        send_mail("VaxiTrack Login Code",body,"vaxitrack@gmail.com",[email],fail_silently=False)
        form = RegForm()

    return render(request, "regpage.html", {'form': form})
