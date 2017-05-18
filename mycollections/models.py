from django.db import models


# Create your models here.
class ZhiHuCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, unique=True)
    category_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '知乎收藏夹'
        verbose_name_plural = verbose_name


class ZhiHuCollection(models.Model):
    title = models.CharField(max_length=200, verbose_name='问题')
    question_url = models.CharField(max_length=300, verbose_name='问题地址')
    answer_vote = models.CharField(max_length=200, verbose_name='得票数')
    answer_url = models.CharField(max_length=200, unique=True, verbose_name='回答地址')
    answer_content = models.TextField(verbose_name='回答内容')
    author = models.CharField(max_length=200, verbose_name='回答作者')
    author_url = models.CharField(max_length=300, verbose_name='回答作者地址')
    author_img = models.CharField(max_length=300, verbose_name='作者头像')
    category = models.ForeignKey(ZhiHuCategory, verbose_name='分类')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '知乎回答'
        verbose_name_plural = verbose_name
