from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from .models import *


# Register your models here 
class CityAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('id', 'name')
    search_fields = ['name']


class PatoghCategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('id', 'name')
    search_fields = ['name']


class LocationTypesAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('id', 'name')
    search_fields = ['name']
    list_filter = []


class TagsAdmin(admin.ModelAdmin):
    ordering = ['tag']
    list_display = ('tag', 'id')
    search_fields = ['tag']
    list_filter = []


class UserAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ('username', 'last_name', 'email', 'mobile_number', 'gender')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['gender']
    autocomplete_fields = ['city']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'mobile_number', 'password')}),
        (_("اصل"), {'fields': ('birth_date', 'first_name', 'last_name', 'city')}),
        (_("اطلاعت دیگر"), {'fields': ('gender', 'avatar', 'bio', 'score')}),
    )


class PatoghInfoAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name', 'type', 'city', 'creator')
    search_fields = ['creator', 'name', 'city', 'category']
    list_filter = ['type']
    autocomplete_fields = ['city', 'creator', 'category']
    fieldsets = (
        (None, {'fields': ('id', 'creator', 'name', 'type')}),
        (_("آدرس"), {'fields': ('address', 'city')}),
        (_("اطلاعات دیگر"), {'fields': ('category', 'description', 'creation_time', 'profile_image_url')})
    )


class PendingVerifyAdmin(admin.ModelAdmin):
    ordering = ['send_time']
    list_display = ('send_time', 'receptor', 'allowed_try')
    list_filter = ['allowed_try']
    search_fields = ['receptor']
    list_filter = []


class PartyAdmin(admin.ModelAdmin):
    ordering = ['name', 'id']
    list_display = ('name', 'id', 'creator', 'creation_time')
    search_fields = ['creator']
    list_filter = []
    autocomplete_fields = ['creator']
    fieldsets = (
        (None, {'fields': ('id', 'creator_id', 'patogh_id', 'name', 'status')}),
        (_("فیلتر ها"), {'fields': ('start_time', 'end_time', 'gender_filter', 'members_count', 'min_age', 'max_age')}),
        (_("اطلاعات دیگر"), {'fields': ('description', 'tags_id')})
    )


class PatoghAdmin(admin.ModelAdmin):
    ordering = ['patogh_id', 'id']
    list_display = ('patogh_id', 'id', 'start_time', 'end_time')
    search_fields = ['patogh_id']
    list_filter = []
    autocomplete_fields = ['patogh_id']


class PartyMembersAdmin(admin.ModelAdmin):
    ordering = ['p_id', 'g_id']
    list_display = ('p_id', 'g_id', 'status')
    search_fields = ['status']
    list_filter = []
    autocomplete_fields = ['p_id', 'g_id']


class PatoghMembersAdmin(admin.ModelAdmin):
    ordering = ['patogh_id', 'email']
    list_display = ('patogh_id', 'email', 'state', 'time')
    search_fields = ['state']
    list_filter = []
    autocomplete_fields = ['patogh_id', 'email']


class PatoghsCommentsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('sender', 'patogh_id', 'send_time')
    search_fields = ['sender', 'patogh_id']
    list_filter = []
    autocomplete_fields = ['sender', 'patogh_id', 'reply_to']


class reportedPatoghAdmin(admin.ModelAdmin):
    ordering = ['username', 'patogh_id']
    list_display = ('username', 'patogh_id', 'send_time')
    search_fields = ['sender', 'patogh_id']
    list_filter = []
    autocomplete_fields = ['patogh_id', 'username']


class PatoghHaveImagesAdmin(admin.ModelAdmin):
    ordering = ['patogh_id']
    list_display = ('patogh_id', 'status', 'send_time')
    search_fields = ['patogh_id']
    list_filter = ['status']
    autocomplete_fields = ['patogh_id']


class UsersHaveFriendsAdmin(admin.ModelAdmin):
    ordering = ['sender', 'receiver']
    list_display = ('sender', 'receiver', 'state', 'time')
    search_fields = ['sender', 'receiver', 'state']
    list_filter = ['state']
    autocomplete_fields = ['sender', 'receiver']


admin.site.register(City, CityAdmin)
admin.site.register(PatoghCategory, PatoghCategoryAdmin)
admin.site.register(LocationTypes, LocationTypesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PatoghInfo, PatoghInfoAdmin)
admin.site.register(PendingVerify, PendingVerifyAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Patogh, PatoghAdmin)
admin.site.register(PartyMembers, PartyMembersAdmin)
admin.site.register(PatoghMembers, PatoghMembersAdmin)
admin.site.register(PatoghsComments, PatoghsCommentsAdmin)
admin.site.register(reportedPatogh, reportedPatoghAdmin)
admin.site.register(PatoghHaveImages, PatoghHaveImagesAdmin)
admin.site.register(UsersHaveFriends, UsersHaveFriendsAdmin)
