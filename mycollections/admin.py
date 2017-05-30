from django.contrib import admin
from .models import ZhiHuCollection, ZhiHuCategory, CollectionArticle, Collection


# Register your models here.
class ZhiHuCollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']

admin.site.register(ZhiHuCollection, ZhiHuCollectionAdmin)
admin.site.register(ZhiHuCategory)
admin.site.register(Collection)
admin.site.register(CollectionArticle)
