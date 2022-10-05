from django.contrib import admin
from .models import *


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'isim', 'user', 'slug')
    list_display_links= ('id', 'user')
    search_fields = ('isim',)
    list_editable = ('isim',)
    list_per_page = 3
    list_filter = ('isim', 'user')
    readonly_fields = ('slug',)
    
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Account)