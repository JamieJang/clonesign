from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMessage

import os

from . import models

@receiver(post_save,sender=models.Document)
def change_upload_docs(sender,**kwargs):
    document = kwargs['instance']
    docs = document.docs
    origin = docs.path
    docs_path = '/'.join(origin.split('/')[:-1])
    if origin.split(".")[1] != 'pdf':    
        os.system("/Applications/LibreOffice.app/Contents/MacOS/soffice --convert-to pdf --outdir {} {}".format(docs_path, origin))
        conv = origin.split(".")[0] + ".pdf"
        document.docs = "/".join(conv.split("/")[-6:])
        document.save()

    partners = document.partners.all()
    emails = []
    message = "다음 계약서가 도착했습니다.\n http://localhost:8000{}".format(document.docs.url)
    if partners:
        for partner in partners:
            emails.append(partner.email)
        EmailMessage('새로운 계약서', message, to=emails).send()

@receiver(post_save, sender=models.Template)
def change_temp_to_docs(sender,**kwargs):
    template = kwargs['instance']
    os.system("wkhtmltopdf --dpi 480 http://localhost:8000/document/own_template/{} {}/templates/{}.pdf"
        .format(template.pk, settings.MEDIA_ROOT, template.title))
    file = os.path.join(settings.MEDIA_URL, 'templates', template.title+".pdf")
    if not template.filepath:
        template.filepath = file
        template.save()

@receiver(post_delete,sender=models.Template)
def delete_temp(sender,**kwargs):
    template = kwargs['instance']
    filepath = os.path.join(settings.MEDIA_ROOT,'templates',template.title+".pdf")
    os.system("rm -rf {}".format(filepath))


    
