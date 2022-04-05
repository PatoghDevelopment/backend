from django.contrib import admin
from django.utils.translation import gettext as _
from .models import *


class UserAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'username', 'email')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['gender']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_("اصل"), {'fields': ('birth_date', 'first_name', 'last_name', 'province')}),
        (_("اطلاعت دیگر"), {'fields': ('gender', 'avatar', 'bio')}),
    )


class PendingVerifyAdmin(admin.ModelAdmin):
    ordering = ['send_time']
    list_display = ('send_time', 'receptor', 'allowed_try')
    list_filter = ['allowed_try']
    search_fields = ['receptor']


class SupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    search_fields = ['email']


class UsersHaveFriendsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'sender', 'receiver', 'state', 'time')
    search_fields = ['sender', 'receiver', 'state']
    list_filter = ['state']
    autocomplete_fields = ['sender', 'receiver']


class HangoutAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'description')
    search_fields = ['name', 'province', 'gender', 'status', 'price', 'place', 'type']
    list_filter = ['gender']


admin.site.register(User, UserAdmin)
admin.site.register(PendingVerify, PendingVerifyAdmin)
admin.site.register(UsersHaveFriends, UsersHaveFriendsAdmin)
admin.site.register(Support, SupportAdmin)
admin.site.register(Hangout, HangoutAdmin)
admin.site.register(HangoutInvitation)
