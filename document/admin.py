from django.contrib import admin

from . import models

@admin.register(models.Document)
class AdminDocument(admin.ModelAdmin):
    list_display = ('id','creator','docs','status','created_at','updated_at')
    list_display_links = ('id', 'creator', 'docs')
    search_fields = ('creator','docs','status')
    list_filter = ('status','created_at','updated_at','creator')
