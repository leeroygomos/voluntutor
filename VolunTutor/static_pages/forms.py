from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    school = forms.CharField(max_length=30)
    study = forms.CharField(max_length=30)
    degree = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                  'birth_date', 'school', 'study', 'degree', 
                  'password1', 'password2', )


class LogInForm(AuthenticationForm):

    class Meta:
        model = User
        #fields = ('username', 'password', )
