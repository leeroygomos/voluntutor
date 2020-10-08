"""
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Welcome to VolunTutor!")
"""


# pages/views.py
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import RegisterForm, LogInForm
from .models import Profile
from upload.models import Upload, UploadPrivate
import uuid

class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchPageView(TemplateView):
    template_name = 'search.html'

class TestPageView(TemplateView):
    template_name = "helloWorld.html"


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.school = form.cleaned_data.get('school')
            user.profile.study = form.cleaned_data.get('study')
            user.profile.degree = form.cleaned_data.get('degree')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

"""
def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        print(request.POST)
        print(form.is_bound)
        if form.is_valid():
            user = authenticate(aimusername=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = LogInForm()
    return render(request, 'login.html', {'form': form})
"""

def logoutView(request):

    logout(request)
    return redirect('home')

def userlist(request):
    query = Profile.objects.all().exclude(study='')
    search = request.GET.get("search")

    if search != '' and search is not None:
        # query = query.filter(user__first_name= search_first_name)
        query = Profile.objects.filter( Q(first_name__icontains=search) |
                                        Q(last_name__icontains=search) |
                                        Q(school__icontains=search) |
                                        Q(study__icontains=search) |
                                        Q(degree__icontains=search)

                                        )

    return render(request,"search.html",{'Users':query})

def delete(request):
    #deleting user automagically logs them out

    currentUser = request.user
    if currentUser.is_authenticated:
        userInDatabase = User.objects.get(username=currentUser)
        if userInDatabase is not None:
            print("deleting " + str(currentUser))
            userInDatabase.delete()
        else:
            print("No such user, are you a ghost? how are you even authenticated?")
    else:
        print("anonymous user, cannot delete")

    return redirect('home')


def profile(request):
    if request.method == 'POST':
        image_file = request.FILES['image_file']
        image_type = request.POST['image_type']
        if settings.USE_S3:
            if image_type == 'private':
                upload = UploadPrivate(file=image_file)
            else:
                upload = Upload(file=image_file)
            upload.save()
            image_url = upload.file.url
        else:
            fs = FileSystemStorage()

            ext = image_file.name.split('.')[-1]
            _filename = "%s.%s" % (uuid.uuid4(), ext)

            filename = fs.save(_filename, image_file)
            image_url = fs.url(filename)
        return render(request, 'profile.html', {
            'image_url': image_url
        })
    return render(request, 'profile.html')
 