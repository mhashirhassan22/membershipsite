from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
from django.contrib.sites.models import Site
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib.auth.admin import UserAdmin
from django.contrib import auth
from .models import *

User = get_user_model()

class UserInterestInline(admin.TabularInline):
    model = UserInterest
    extra = 3


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = auth_admin.UserAdmin.fieldsets + (("User", {"fields": ("phone", "business_name", "website", "address","country","state","city","timezone","servicearea")}),)
    inlines = [ UserInterestInline, ]


class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(ServiceArea, ServiceAreaAdmin)


class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Interest, InterestAdmin)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('title','description')

admin.site.register(FAQ, FAQAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email','message','is_resolved')
    list_editable = ('is_resolved',)

admin.site.register(Contact, ContactAdmin)


class SubAdmin(admin.ModelAdmin):
    list_display = ('membership','user','is_active','created_at')

admin.site.register(Subscription, SubAdmin)


admin.site.register(MembershipPlan)