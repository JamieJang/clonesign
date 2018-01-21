from django.db import models
from user import models as user_models
from datetime import datetime

import os
import sys

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class Folder(Timestamp):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name

class Document(Timestamp):
    def generate_filename(self,filename):
        today = datetime.today()
        return "document/{}/{}/{}/{}/{}".format(self.creator.username, today.year, today.month, today.day, filename)

    STATUS_LIST = (
        ('서명 전', '서명 전'),
        ('내 서명 필요','내 서명 필요'),
        ('상대 서명 필요','상대 서명 필요'),
        ('완료','완료'),
        ('거절','거절'),
        ('취소','취소'),
    )

    creator = models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE, related_name="docs_myself")
    docs = models.FileField(upload_to=generate_filename)
    filename = models.CharField(max_length=140,blank=True)
    partners = models.ManyToManyField(user_models.MyUser,related_name="docs_by_partners")
    status = models.CharField(max_length=50, choices=STATUS_LIST, default=STATUS_LIST[0][0])
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return "{} / {} / {}".format(self.docs, self.status, self.creator)

    def save(self):
        name = self.docs.name.split('/')[-1]
        name = name.split(".")[0]
        self.filename = name.encode()
        super(Document,self).save()

    class Meta:
        ordering = ['-updated_at']

class Template(Timestamp):
    title = models.CharField(max_length=140)
    content = models.TextField()
    creator = models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE, related_name="temp_myself")
    partner = models.ManyToManyField(user_models.MyUser, related_name="temp_partners")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
