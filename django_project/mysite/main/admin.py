from django.contrib import admin
from .models import University, Country


class AdminUniv(admin.ModelAdmin):
    search_fields = ['name', 'country', 'rank']

admin.site.register(University, AdminUniv)

class AdminCount(admin.ModelAdmin):
    search_fields = ['id', 'name']

admin.site.register(Country, AdminCount)

