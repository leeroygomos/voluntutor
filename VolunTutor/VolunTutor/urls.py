"""VolunTutor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('static_pages.urls')),
    path('admin/', admin.site.urls),
]

# pages/urls.py
from django.urls import path
from static_pages.views import HomePageView, userlist, register, login, logoutView, delete, profile
from chat.views import chat
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('profile/', profile, name='profile'),
    path('search/', userlist, name='search'),
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", logoutView, name="logout"),
    path("delete/", delete, name="delete"),
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('chat/', chat, name='chat')
]

