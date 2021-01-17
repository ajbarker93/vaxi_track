from django.urls import path, include

from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    path('userpage/', views.userpage, name="userpage"),
    path('vaxpage/', views.vaxpage, name="vaxpage"),
    path('regpage/', views.regpage, name="regpage"),
]