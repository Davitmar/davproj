from django.contrib import admin
from .models import Authors, Quotas, Tags


class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author']
    search_fields = ['author']


class QuotasAdmin(admin.ModelAdmin):
    list_display = ['pk', 'quota', 'author', 'user']
    search_fields = ['quota', 'author', 'tag']


class TagsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag']
    search_fields = ['tag']


admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Quotas, QuotasAdmin)
admin.site.register(Tags, TagsAdmin)

#username:davit, password:admin1