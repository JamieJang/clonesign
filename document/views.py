from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.db.models import Q

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

        default_status = "모든상태"
        status_list = [ x[0] for x in models.Document.STATUS_LIST]

        return render(request, 'document/index.html',{'total_docs':total_docs,
                                                        'self_docs':self_docs,
                                                        'part_docs':part_docs,
                                                        'docs':docs,
                                                        'status_list':status_list,
                                                        "default_status" : default_status})

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
        try:
            partner = user_models.MyUser.objects.get(username=name,email=email)
            new_docs.partners.add(partner)
            new_docs.save()
        except user_models.MyUser.DoesNotExist:
            return redirect("document:upload-docs")

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

        status_list = [x[0] for x in models.Document.STATUS_LIST]
        default_status = "모든상태"

        return render(request, 'document/index.html', {'total_docs': total_docs,
                                                       'self_docs': self_docs,
                                                       'part_docs': part_docs,
                                                       'docs': docs,
                                                       'status_list': status_list,
                                                       "default_status": default_status})

class docsByPartner(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("/")

        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        docs = user.docs_by_partners.all()

        status_list = [x[0] for x in models.Document.STATUS_LIST]
        default_status = "모든상태"

        return render(request, 'document/index.html',{'total_docs':total_docs,
                                                        'self_docs':self_docs,
                                                        'part_docs':part_docs,
                                                        'docs': docs,
                                                        'status_list': status_list,
                                                        "default_status": default_status})

class docsByStatus(View):
    def get(self,request,status):

        status = status.replace("-"," ")
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        docs = list(models.Document.objects.filter(creator=user, status=status))
        docs += list(user.docs_by_partners.all().filter(status=status))

        default_status = status
        status_list = [x[0] for x in models.Document.STATUS_LIST if x[0] != default_status]
        

        return render(request, 'document/index.html', {'total_docs': total_docs,
                                                       'self_docs': self_docs,
                                                       'part_docs': part_docs,
                                                       'docs': docs,
                                                       'status_list': status_list,
                                                       "default_status" : default_status})

class docsByKeyword(View):
    def get(self,request,keyword):
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        docs = []
        docs = list(models.Document.objects.filter(Q(creator=user),  Q(partners__username__icontains=keyword) |
                                                   Q(creator__username__icontains=keyword) | Q(filename__icontains=keyword)).distinct())
        docs += list(user.docs_by_partners.all().filter(Q(partners__username__icontains=keyword) |
                                                        Q(creator__username__icontains=keyword) | Q(filename__icontains=keyword)).distinct())

        print(keyword);

        default_status = "모든상태"
        status_list = [x[0] for x in models.Document.STATUS_LIST]

        return render(request, 'document/index.html', {'total_docs': total_docs,
                                                       'self_docs': self_docs,
                                                       'part_docs': part_docs,
                                                       'docs': docs,
                                                       'status_list': status_list,
                                                       "default_status": default_status})
