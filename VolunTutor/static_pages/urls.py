"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
"""


# pages/urls.py
from django.urls import path

from .views import HomePageView, SearchPageView, register, login, delete, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('search/', SearchPageView.as_view(), name='search'),
    path("register/", register, name="register"),
    #path("login/", login, name="login"),
    path("delete/", delete, name="delete"),
    path('', HomePageView.as_view(), name='home'),
]


