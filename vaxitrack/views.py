from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def userpage(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "userpage.html")

def vaxpage(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "vaxpage.html")

def regpage(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "regpage.html")
