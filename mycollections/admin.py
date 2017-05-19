from django.contrib import admin
from .models import ZhiHuCollection, ZhiHuCategory


# Register your models here.
class ZhiHuCollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']

admin.site.register(ZhiHuCollection, ZhiHuCollectionAdmin)
admin.site.register(ZhiHuCategory)
