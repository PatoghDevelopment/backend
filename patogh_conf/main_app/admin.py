from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from .models import *


# Register your models here.
class GatheringInline(admin.StackedInline):
    model = Gathering
    extra = 1
    show_change_link = True

class PatoghInline(admin.StackedInline):
    model = Patogh
    extra = 1
    show_change_link = True

class UserCommentInline(TabularInline):
    model = PatoghsComments
    extra = 1
    show_change_link = True

class CityAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name','id')
    search_fields = ['name']
    
class PatoghCategoryAdmin(admin.ModelAdmin):
    ordering = ['category']
    list_display = ('category','id')
    search_fields = ['category']

class LocationTypesAdmin(admin.ModelAdmin):
    ordering = ['label']
    list_display = ('label','id')
    search_fields = ['label']
    list_filter = []


class TagsAdmin(admin.ModelAdmin):
    ordering = ['tag']
    list_display = ('tag','id')
    search_fields = ['tag']
    inlines = [GatheringInline,PatoghInline]
    list_filter = []

    
class UserAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ('username','fullname','email','phone','gender')
    search_fields = ['username','fullname','email']
    list_filter = ['gender']
    inlines = [UserCommentInline]
    autocomplete_fields = ['city']
    fieldsets = (
        (None, {'fields': ('username','email','phone','password')}),
        (_("اصل"), {'fields': ('birthdate','fullname','city')}),
        (_("اطلاعت دیگر"),{'fields': ('gender','profile_image_url','bio')}),
        (_("اطلاعات امنیتی"), {'fields': ('otp','is_confirmed','expire_time')}),
    )

class PatoghAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name','status','city','creator_id')
    search_fields = ['creator_id','name','city','category']
    list_filter = ['status','is_telephone_verified','wifi','poz']
    autocomplete_fields = ['city','creator_id','location_type','tags_id','category']
    fieldsets = (
        (None, {'fields': ('id','creator_id','name','status')}),
        (_("اعتبارسنجی پاتوق"), {'fields': ('telephone','is_telephone_verified')}),
        (_("آدرس"),{'fields': ('address','longitude','latitude','city','location_type')}),
        (_("امکانات پاتوق"),{'fields': ('wifi','poz')}),
        (_("اطلاعات دیگر"),{'fields': ('category','description','profile_image_url','tags_id')})
    )
class PendingVerifyAdmin(admin.ModelAdmin):
    ordering = ['send_time']
    list_display = ('send_time','receptor','allowed_try')
    list_filter = ['allowed_try']
    search_fields = ['receptor']
    list_filter = []
    autocomplete_fields = ['receptor']

class UsersPermisionAdmin(admin.ModelAdmin):
    ordering = ['label']
    list_display = ('label','id')
    search_fields = ['label']
    list_filter = []

class GatheringHaveMemberAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ('username_id','status','g_id')
    search_fields = ['username']
    list_filter = ['status']
    autocomplete_fields = ['g_id','username']

class GatheringAdmin(admin.ModelAdmin):
    ordering = ['name','id']
    list_display = ('name','patogh_id','creator_id','members_count')
    search_fields = ['username']
    list_filter = ['status','gender_filter']
    autocomplete_fields = ['creator_id','patogh_id','tags_id']
    fieldsets = (
        (None, {'fields': ('id','creator_id','patogh_id','name','status')}),
        (_("فیلتر ها"), {'fields': ('start_time','end_time','gender_filter','members_count','min_age','max_age')}),
        (_("اطلاعات دیگر"),{'fields': ('description','tags_id')})
    )
class JoinGatheringRequestAdmin(admin.ModelAdmin):
    ordering = ['username','g_id']
    list_display = ('username','status','g_id')
    search_fields = ['username','g_id']
    list_filter = ['status']
    autocomplete_fields = ['g_id','username']

class PatoghsCommentsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('sender','patogh_id','send_time')
    search_fields = ['sender','patogh_id']
    list_filter = []
    autocomplete_fields = ['sender','patogh_id','reply_to']

class reportedPatoghAdmin(admin.ModelAdmin):
    ordering = ['username','patogh_id']
    list_display = ('username','patogh_id','send_time')
    search_fields = ['sender','patogh_id']
    list_filter = []
    autocomplete_fields = ['patogh_id','username']

class PatoghHaveImagesAdmin(admin.ModelAdmin):
    ordering = ['patogh_id']
    list_display = ('patogh_id','status','send_time')
    search_fields = ['patogh_id']
    list_filter = ['status']
    autocomplete_fields = ['patogh_id']

class UsersHavePermisionsAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ('username','permision_id')
    search_fields = ['permision_id','username']
    list_filter = []
    autocomplete_fields = ['permision_id','username']

class GatheringScheduallAdmin(admin.ModelAdmin):
    ordering = ['g_id']
    list_display = ('g_id','Sa','Su','Mo','Tu','We','Th','Fr')
    search_fields = ['g_id']
    list_filter = ['Sa','Su','Mo','Tu','We','Th','Fr']
    autocomplete_fields = ['g_id']



admin.site.register(User, UserAdmin)
admin.site.register(City ,CityAdmin)
admin.site.register(PatoghCategory ,PatoghCategoryAdmin)
admin.site.register(LocationTypes, LocationTypesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Patogh, PatoghAdmin)
admin.site.register(PendingVerify, PendingVerifyAdmin)
admin.site.register(UsersPermision, UsersPermisionAdmin)
admin.site.register(GatheringHaveMember, GatheringHaveMemberAdmin)
admin.site.register(Gathering, GatheringAdmin)
admin.site.register(JoinGatheringRequest, JoinGatheringRequestAdmin)
admin.site.register(PatoghsComments, PatoghsCommentsAdmin)
admin.site.register(reportedPatogh, reportedPatoghAdmin)
admin.site.register(PatoghHaveImages, PatoghHaveImagesAdmin)
admin.site.register(UsersHavePermisions, UsersHavePermisionsAdmin)
admin.site.register(GatheringScheduall, GatheringScheduallAdmin)



