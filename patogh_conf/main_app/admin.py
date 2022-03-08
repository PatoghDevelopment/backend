from django.contrib import admin
from django.utils.translation import gettext as _
from .models import *


class CityAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name')
    search_fields = ['name']


class UserAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'username', 'email')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['gender']
    autocomplete_fields = ['city']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_("اصل"), {'fields': ('birth_date', 'first_name', 'last_name', 'city')}),
        (_("اطلاعت دیگر"), {'fields': ('gender', 'avatar', 'bio')}),
    )


class PendingVerifyAdmin(admin.ModelAdmin):
    ordering = ['send_time']
    list_display = ('send_time', 'receptor', 'allowed_try')
    list_filter = ['allowed_try']
    search_fields = ['receptor']


class SupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


class PatoghCategoryAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name')
    search_fields = ['name']


class PatoghAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'type', 'city', 'creator')
    search_fields = ['creator', 'name', 'city', 'category']
    list_filter = ['type']
    autocomplete_fields = ['city', 'creator', 'category']
    fieldsets = (
        (None, {'fields': ('id', 'creator', 'name', 'type')}),
        (_("آدرس"), {'fields': ('address', 'city')}),
        (_("اطلاعات دیگر"), {'fields': ('category', 'description', 'creation_time', 'profile_image')})
    )
    readonly_fields = ['creation_time']


class PatoghMembersAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'patogh_id', 'email', 'state', 'time')
    search_fields = ['state']
    autocomplete_fields = ['patogh_id', 'email']


class UsersHaveFriendsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'sender', 'receiver', 'state', 'time')
    search_fields = ['sender', 'receiver', 'state']
    list_filter = ['state']
    autocomplete_fields = ['sender', 'receiver']


admin.site.register(City, CityAdmin)
admin.site.register(PatoghCategory, PatoghCategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PendingVerify, PendingVerifyAdmin)
admin.site.register(Patogh, PatoghAdmin)
admin.site.register(PatoghMembers, PatoghMembersAdmin)
admin.site.register(UsersHaveFriends, UsersHaveFriendsAdmin)
admin.site.register(Support, SupportAdmin)
