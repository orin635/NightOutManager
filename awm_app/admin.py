from django.contrib import admin
from .models import Profile, Group

admin.site.register(Profile)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('groupCode', 'pubNames')
