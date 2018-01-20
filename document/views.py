from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

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

class Profile(View):
    def get(self,request):
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs

        password_form = PasswordChangeForm(user)

        return render(request, 'document/profile.html', {'total_docs': total_docs,
                                                         'self_docs': self_docs,
                                                         'part_docs': part_docs, 
                                                         'user':user,
                                                         'password_form':password_form})

class ChangeUsername(View):
    def post(self,request):
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        
        password_form = PasswordChangeForm(user)

        new_username = request.POST['username']
        if new_username:
            print(user.username)
            user.username = new_username
            print(user.username)
            user.save()
            messages.success(request, "이름을 성공적으로 변경하였습니다.")
            return redirect("document:profile")
        else:
            message.error(request, "다시 시도해주기시 바랍니다.")
        
        return render(request, 'document/profile.html', {'total_docs': total_docs,
                                                         'self_docs': self_docs,
                                                         'part_docs': part_docs,
                                                         'user': user,
                                                         'password_form': password_form})

        

class ChangePassword(View):
    def post(self,request):
        user = request.user
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs
        password_form = PasswordChangeForm(user,request.POST)
        if password_form.is_valid():
            changed_user = password_form.save()
            update_session_auth_hash(request, changed_user)
            messages.success(request,"비밀번호를 성공적으로 변경하였습니다.")
            return redirect("document:profile")
        else:
            messages.error(request,"다시 시도해주시기 바랍니다.")
        
        return render(request, 'document/profile.html', {'total_docs': total_docs,
                                                         'self_docs': self_docs,
                                                         'part_docs': part_docs,
                                                         'user': user,
                                                         'password_form': password_form})
