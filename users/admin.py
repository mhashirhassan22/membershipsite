from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib.auth.admin import UserAdmin
from django.contrib import auth

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
    # fieldsets = (("User", {"fields": ("phone", "business_name", "website")}),) + admin.UserAdmin.fieldsets

