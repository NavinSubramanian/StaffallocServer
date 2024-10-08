from django.contrib import admin
from .models import *

class UsersAdmin(admin.ModelAdmin):
    list_display=('name','password','department','email')
    search_fields=['name','password','department','email']

class StaffAdmin(admin.ModelAdmin):
    list_display=('name','designation','department','gender','subcode')
    search_fields=['name','designation','department','gender','subcode']

class RoomsAdmin(admin.ModelAdmin):
    list_display=['roomno']
    search_fields=['roomno']

class ProfileAdmin(admin.ModelAdmin):
    list_display=('username','department')
    search_fields=('username','department')

admin.site.register(Users,UsersAdmin)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Rooms,RoomsAdmin)
admin.site.register(Profile,ProfileAdmin)
