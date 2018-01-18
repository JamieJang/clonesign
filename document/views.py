from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class index(View):
    def get(self,request):
        print(request.user)
        return HttpResponse("DOCUMENT")