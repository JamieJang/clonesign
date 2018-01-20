from django import forms

from . import models

class DocsForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ('docs',)