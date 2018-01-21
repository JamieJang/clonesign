from django.contrib import admin

from . import models

@admin.register(models.Document)
class AdminDocument(admin.ModelAdmin):
    list_display = ('id','creator','filename','docs','status','created_at','updated_at')
    list_display_links = ('id', 'creator', 'docs')
    search_fields = ('filename',)
    list_filter = ('status','created_at','updated_at','creator')

@admin.register(models.Template)
class AdminTemplate(admin.ModelAdmin):
    list_display = ("title","creator")
    
