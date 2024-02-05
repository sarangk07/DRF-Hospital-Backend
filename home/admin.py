from django.contrib import admin
from home.models import UserData
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username') 

admin.site.register(UserData, UserAdmin)


