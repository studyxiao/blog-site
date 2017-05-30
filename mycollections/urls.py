from django.conf.urls import url
from .views import index, detail, test


app_name = 'collections'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^detail/(?P<article_id>[0-9]+)$', detail, name='detail'),
    url(r'^test$', test, name='test'),
]
