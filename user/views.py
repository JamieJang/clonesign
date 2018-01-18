from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from . import forms

class signup(View):
    def get(self,request):
        form = forms.SignupForm()
        return render(request, 'user/signup.html', {"form":form})
