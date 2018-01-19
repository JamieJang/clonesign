from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from . import models

class index(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("/")
        
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        docs = models.Document.objects.filter(creator=user)


        return render(request, 'document/index.html',{'total_docs':total_docs,
                                                        'self_docs':self_docs,
                                                        'part_docs':part_docs,
                                                        'docs':docs})