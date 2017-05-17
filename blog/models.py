from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Category(models.Model):
    """
    分类
    name: 分类名称
    """
    name = models.CharField(max_length=100, verbose_name='分类名称')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签
    name: 标签名称
    """
    name = models.CharField(max_length=100, verbose_name='标签名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
        文章
        title: 文章名称
        content: 文章内容
        created_time: 创建时间
        modified_time: 修改时间
        excerpt: 摘要，允许为空
        category: 分类，一对多
        tags: 标签，多对多
        author: 作者，一对多
        """
    title = models.CharField(max_length=100, verbose_name='题目')
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(default=datetime.now(), verbose_name='创建时间')
    modified_time = models.DateTimeField(default=datetime.now, verbose_name='修改时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要')
    category = models.ForeignKey(Category, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    author = models.ForeignKey(User, verbose_name='作者')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    # def get_absolute_url(self):
    #     return reverse('blog:detail', kwargs={'pk': self.pk})
