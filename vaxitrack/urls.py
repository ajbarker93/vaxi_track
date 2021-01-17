from django.urls import path, include

from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    # path('', views.userpage, name="userpage"),
    path('userpage/', views.userpage, name="userpage"),
    # path("userpage", views.userpage, name="userpage"),
    # path("userpage.html", views.userpage, name="userpage"),
    path('vaxpage/', views.vaxpage, name="vaxpage"),
    # path("vaxpage", views.vaxpage, name="vaxpage"),
    # path("vaxpage.html", views.vaxpage, name="vaxpage"),
    path('regpage/', views.regpage, name="regpage"),
    # path("regpage", views.regpage, name="regpage"),
    # path("regpage.html", views.regpage, name="regpage")
]
