from django.contrib import admin
from home.models import UserData , Doctor

# Register your models here.



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , ]

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username') 

admin.site.register(UserData, UserAdmin)



