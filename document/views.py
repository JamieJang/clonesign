from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

class index(View):
    def get(self,request):

        if not request.user.is_authenticated:
            return redirect("/")
        return HttpResponse("DOCUMENT")