from django.shortcuts import render
from .models import ZhiHuCollection, ZhiHuCategory


def index(request):
    context = {}
    article_list = []
    categories = ZhiHuCategory.objects.all()
    for category in categories:
        art = ZhiHuCollection.objects.filter(category=category)
        item = {'category': category.name, 'articles': list(art)}
        article_list.append(item)
    context['article_list'] = article_list
    return render(request, 'mycollections/index.html', context)


def detail(request, article_id):
    context = {}
    article = ZhiHuCollection.objects.get(id=article_id)
    article.answer_content = article.answer_content.replace('\\"', '"')
    article.answer_content = article.answer_content.replace("\\'", "'")
    context['article'] = article
    return render(request, 'mycollections/detail.html', context)
