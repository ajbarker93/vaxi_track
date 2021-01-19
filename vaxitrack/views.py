from django.shortcuts import render
from django.http import HttpResponse

from .models import Centre, User
from .forms import BuildForm
from .forms import LogForm

import numpy as np

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def userpage(request):
    # return HttpResponse('Hello from Python!')
    user = User.objects.all()[0]
    cents = Centre.objects.all()
    dists = [ np.linalg.norm(user.location - c.location, ord=2) for c in cents ]
    cent_dists = list(zip(cents, dists))
    return render(request, "userpage.html", {'cent_dists': cent_dists})

def vaxpage(request):
    # return HttpResponse('Hello from Python!')
    form = LogForm()
    user = User.objects.all()[0]
    cents = Centre.objects.all()
    dists = [ np.linalg.norm(user.location - c.location, ord=2) for c in cents ]
    cent_dists = list(zip(cents, dists))
    return render(request, "vaxpage.html", {'form': form})

def regpage(request):
    form = BuildForm()
    return render(request, "regpage.html",{'form': form })
