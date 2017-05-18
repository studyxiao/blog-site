from django.contrib import admin
from django import forms

from pagedown.widgets import AdminPagedownWidget

from .models import Article, Category, Tag


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
