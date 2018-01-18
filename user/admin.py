from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from . import models

@admin.register(models.MyUser)
class UserAdmin(admin.ModelAdmin):
    """Define admin model for custom User model with no email field."""

   
    list_display = ('email', 'username','is_admin')
    search_fields = ('email', 'username')
    ordering = ('email',)

