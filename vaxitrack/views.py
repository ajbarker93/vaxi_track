from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from django_q import tasks as qtasks
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Centre, User, Counter
from .forms import LogForm, UserForm, RegForm
from .tasks import find_and_assign

def index(request):

    ncents,nvax,npats = Counter.read()
    return render(request, "index.html", {'ncents': f"{ncents:,}",'nvax': f"{nvax:,}"})


def success(request):

    return render(request, "success.html")


def userpage(request):

    form = UserForm(request.POST)

    if form.is_valid():
        age = str(form['age'].value())
        pc = str(form['postcode'].value())
        email = str(form['email'].value())
        usr = User.create(pc,email,age)
        Counter.increment(centres=0, vaccines=0, patients=1)
        usr.send_email()
        form = UserForm()
        return redirect('success')

    return render(request, "userpage.html", {'form': form})


def vaxpage(request):

    form = LogForm(request.POST)

    if form.is_valid():
        data_dict = form.cleaned_data
        doses = data_dict['doses_available']
        ttime = data_dict['available_at']
        ttype = data_dict['vax_type']
        vtid = data_dict['VaxiTrack_ID']
        vtid = int(vtid)
        cent = Centre.objects.filter(id__exact=vtid).get()

        if cent.id > 0:
            cent.set_doses(doses)
            cent.set_time_available(ttime)
            cent.set_type(ttype)
            cent.log_email()
            #redirect('app:success')
        else:
            raise ValueError("No centre with that ID is recognised.")

        # this is where you add the assign_doses task to the queue
        qtasks.async_task(find_and_assign, cent.id, doses)

        form = LogForm()
        return redirect('success')

    return render(request, "vaxpage.html", {'form': form})


def regpage(request):

    form = RegForm(request.POST)

    if form.is_valid():
        data_dict = form.cleaned_data
        name = data_dict['name']
        pc = data_dict['postcode']
        email = data_dict['email']
        cent = Centre.create(name,pc,email)
        cent.send_email()
        form = RegForm()
        return redirect('success')


    return render(request, "regpage.html", {'form': form})
