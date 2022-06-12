from django.contrib import admin
from .models import Authors, Quotas, Tags, UsersPhotos, Messege


class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author']
    search_fields = ['author']


class QuotasAdmin(admin.ModelAdmin):
    list_display = ['pk', 'quota', 'author', 'user']
    search_fields = ['quota', 'author', 'tag']


class TagsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag']
    search_fields = ['tag']

class MessegeAdmin(admin.ModelAdmin):
    list_display = ['messege', 'sender', 'reciever']
    search_fields = ['messege', 'sender', 'reciever']

class UserPhotosAdmin(admin.ModelAdmin):
    list_display = ['comment', 'image']
    search_fields = ['comment']


admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Quotas, QuotasAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Messege, MessegeAdmin)
admin.site.register(UsersPhotos, UserPhotosAdmin)

#username:davit, password:admin1