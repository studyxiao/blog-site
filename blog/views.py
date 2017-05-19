from django.shortcuts import render, get_object_or_404
from .models import Article
import markdown


# Create your views here.
def index(request):
    context = {}
    articles = Article.objects.all()
    context['articles'] = articles
    return render(request, 'blog/index.html', context)


def blog_detail(request, pk):
    context = {}
    article = get_object_or_404(Article, pk=pk)
    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc'
                                        ])
    context['article'] = article
    return render(request, 'blog/detail.html', context)
