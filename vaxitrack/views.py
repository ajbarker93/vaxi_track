from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django_q import tasks as qtasks
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Centre, User, Counter
from .forms import LogForm, UserForm, RegForm

import numpy as np
from random import randint

def index(request):

    ncents, nvax, npat = Counter.read()
    return render(request, "index.html")


def userpage(request):

    form = UserForm(request.POST)

    if form.is_valid():
        age = str(form['age'].value())
        pc = str(form['postcode'].value())
        email = str(form['email'].value())
        usr = User.create(pc,email,age)
        usr.send_email()
        form = UserForm()

    return render(request, "userpage.html", {'form': form})


def vaxpage(request):

    form = LogForm(request.POST)

    if form.is_valid():

        data_dict = form.cleaned_data
        doses = data_dict['doses_available']
        ttime = data_dict['available_at']
        ttype = data_dict['vax_type']
        iid = data_dict['VaxiTrack_ID']
        cent = Centre.objects.filter(VaxiTrack_ID__exact=iid).get()
        cent.set_doses(doses)
        cent.set_time_available(ttime)
        cent.set_type(ttype)
        cent.log_email()
        form = LogForm()

    return render(request, "vaxpage.html", {'form': form})


def regpage(request):

    form = RegForm(request.POST)

    if form.is_valid():
        data_dict = form.cleaned_data
        pc = data_dict['postcode']
        email = data_dict['email']
        cent = Centre.create(pc,email)
        cent.send_email()
        form = RegForm()


    return render(request, "regpage.html", {'form': form})
