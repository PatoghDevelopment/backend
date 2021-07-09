from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(City)
admin.site.register(LocationTypes)
admin.site.register(Tags)
admin.site.register(Users)
admin.site.register(Patogh)
admin.site.register(PendingVerify)
admin.site.register(UsersPermision)
admin.site.register(GatheringHaveMember)
admin.site.register(Gathering)
admin.site.register(JoinGatheringRequest)
admin.site.register(PatoghsComments)
admin.site.register(reportedPatogh)
admin.site.register(PatoghHaveImages)
admin.site.register(UsersHavePermisions)
admin.site.register(GatheringScheduall)
