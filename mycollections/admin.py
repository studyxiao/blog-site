from django.contrib import admin
from .models import ZhiHuCollection

# Register your models here.
class ZhiHuCollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']

admin.site.register(ZhiHuCollection, ZhiHuCollectionAdmin)
