from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = models.MyUser
        fields = ('email', 'username', 'password1', 'password2')

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.MyUser
        fields = ('email','password')
