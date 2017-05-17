from django.conf.urls import url
from .views import index, blog_detail

app_name = 'blog'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^detail/(?P<pk>[0-9]+)$', blog_detail, name='blog_detail'),
]
