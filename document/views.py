from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from . import models, forms
from user import models as user_models


class index(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("/")
        
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        docs = list(models.Document.objects.filter(creator=user))
        docs += list(user.docs_by_partners.all())

        return render(request, 'document/index.html',{'total_docs':total_docs,
                                                        'self_docs':self_docs,
                                                        'part_docs':part_docs,
                                                        'docs':docs})

class UploadDocs(View):
    def get(self, request):
        form = forms.DocsForm()
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        return render(request, 'document/upload.html', {'total_docs': total_docs,
                                                        'self_docs': self_docs,
                                                        'part_docs': part_docs, 
                                                        "form": form})

    def post(self,request):
        docs = request.FILES['docs']
        user = request.user
        new_docs = models.Document(creator=user, docs=docs)
        new_docs.save()

        name = request.POST['username']
        email = request.POST['email']
        partner = user_models.MyUser.objects.get(username=name,email=email)
        new_docs.partners.add(partner)
        new_docs.save()

        return redirect("document:docu-index")


class selfDocs(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("/")

        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        docs = models.Document.objects.filter(creator=user)

        return render(request, 'document/index.html', {'total_docs': total_docs,
                                                       'self_docs': self_docs,
                                                       'part_docs': part_docs,
                                                       'docs': docs})

class docsByPartner(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("/")

        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        docs = user.docs_by_partners.all()

        return render(request, 'document/index.html',{'total_docs':total_docs,
                                                        'self_docs':self_docs,
                                                        'part_docs':part_docs,
                                                        'docs':docs})
