from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from operator import attrgetter

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

        docs = sorted(docs, key=attrgetter("updated_at"), reverse=True)

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
        print("docs:",docs, "type:",type(docs))
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
        docs = models.Document.objects.filter(
            creator=user).order_by("-updated_at")

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
        docs = user.docs_by_partners.all().order_by("-updated_at")

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

        docs = sorted(docs, key=attrgetter("updated_at"), reverse=True)

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

        docs = sorted(docs, key=attrgetter("updated_at"), reverse=True)

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
            user.username = new_username
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

class DeleteDocs(View):
    def get(self,request,pk):
        user = request.user
        doc = models.Document.objects.get(pk=pk)
        if doc.creator == user:
            filename = doc.filename
            doc.delete()
            messages.success(request,"Complete delete {}".format(filename))
            return redirect("document:docu-index")
        else:
            messages.error(request, "No Authorization")
            return redirect("document:docu-index")


class OwnTemplate(View):
    def get(self,request):
        user = request.user
        temps = models.Template.objects.filter(creator=user)
        self_docs = user.self_docs_count
        part_docs = user.part_docs_count
        total_docs = self_docs + part_docs

        return render(request, 'document/own_template.html', {'total_docs': total_docs,
                                                              'self_docs': self_docs,
                                                              'part_docs': part_docs, 
                                                              'temps':temps,})

class CreateOwnTemplate(View):
    def get(self,request):
        return render(request,'document/create_template.html')

    def post(self,request):
        title = request.POST['title']
        content = request.POST['content']
        name = request.user.username
        email = request.user.email
        partner_name = request.POST['partner_name']
        partner_email = request.POST['partner_email']

        try:
            creator = user_models.MyUser.objects.get(username=name,email=email)
        except user_models.MyUser.DoesNotExist:
            messages.error(request, "해당 유저가 존재하지 않습니다")
            return redirect("document:own_template")

        try:
            partner = user_models.MyUser.objects.get(username=partner_name,email=partner_email)
        except user_models.MyUser.DoesNotExist:
            messages.error(request, "해당 유저가 존재하지 않습니다")
            return redirect("document:own_template")
        
        temp = models.Template.objects.create(title=title,content=content,creator=creator)
        temp.partner.add(partner)
        temp.save()

        return redirect("document:own_template")


class DetailOwnTemplate(View):
    def get(self,request,pk):
        user = request.user
        try:
            temp = models.Template.objects.get(pk=pk)
        except models.Template.DoesNotExist:
            return redirect("document:own_template")
        
        return render(request, 'document/detail_template.html', {"temp": temp})
        

class DeleteTemplate(View):
    def get(self,request,pk):
        user = request.user
        try:
            temp = models.Template.objects.get(pk=pk)
            if temp.creator == user:
                temp.delete()
            return redirect("document:own_template")
        except models.Template.DoesNotExist:
            return redirect("document:own_template")
        
