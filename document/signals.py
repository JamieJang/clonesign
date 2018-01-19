from django.db.models.signals import post_save
from django.dispatch import receiver

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