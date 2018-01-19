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
        print("filename:",filename)
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
    partners = models.ManyToManyField(user_models.MyUser,related_name="docs_by_partners")
    status = models.CharField(max_length=50, choices=STATUS_LIST, default=STATUS_LIST[0][0])
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return "{} / {} / {}".format(self.docs, self.status, self.creator)

    @property
    def get_filename(self):
        name = self.docs.name.split('/')[-1]
        return name