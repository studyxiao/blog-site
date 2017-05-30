# coding:utf-8

import time

from selenium import webdriver

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../blog'))  # 把包添加到系统目录
import pymysql
pymysql.install_as_MySQLdb()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temporal.settings')
import django
django.setup()

from mycollections.models import Collection, CollectionArticle

juejin_home = 'https://juejin.im/'
driver = webdriver.PhantomJS()


def get_user_collection_url():
    """
    获得用户收藏夹地址url,暂时直接返回自己的
    :return:
    """
    return 'https://juejin.im/user/57f248a3a0bb9f0058092887/collection'  # 中间的一串数字和字母是要获取的用户信息


def get_collection_urls():
    """
    获得所有收藏夹的地址
    :return:
    """
    collection_urls = []
    user_like_url = get_user_collection_url()
    driver.get(user_like_url)
    time.sleep(2)
    like_num = driver.find_element_by_xpath('//*[@id="juejin"]/div[2]/main/div[2]/div/header/div/div/div[1]').text
    print(like_num)
    collections = driver.find_elements_by_xpath('//div[@class="one-collection"]/a')
    titles = driver.find_elements_by_xpath('//div[@class="content"]/div[@class="title"]')
    for collection, title in zip(collections, titles):
        collection_url = collection.get_attribute('href')
        collection_urls.append(collection_url)
        name = title.text
        category = 'juejin'
        item = {
            'name': name,
            'collection_url': collection_url,
            'category': category,
        }
        categories = Collection.objects.filter(collection_url=collection_url)
        if categories:
            # 存在则覆盖
            categories[0].name = name
            categories[0].collection_url = collection_url
            categories[0].category = category
            categories[0].save()
            print('已修改')
        else:
            # 不存在则创建
            category = Collection(name=name, collection_url=collection_url, category=category)
            category.save()

    return collection_urls


def get_per_collection(collection_url):
    driver.get(collection_url)
    collection = Collection.objects.get(collection_url=collection_url)
    time.sleep(2)

    authors = driver.find_elements_by_xpath('//div[@class="user-popover-box"]/a')
    articles = driver.find_elements_by_xpath('//div[@class="info-row title-row"]/a')
    for article, author in zip(articles, authors):
        article_url = article.get_attribute('href')
        article_title = article.text
        author_name = author.text
        print(article_url + ' ' + article_title + ' ' + author_name)
        item = {
            'title': article_title,
            'article_url': article_url,
            'author': author_name,
            'collection': collection
        }
        collection_article = CollectionArticle.objects.filter(article_url=article_url)
        if collection_article:
            # 存在则覆盖
            collection_article[0].title = article_title
            collection_article[0].article_url = article_url
            collection_article[0].author = author_name
            collection_article[0].collection = collection
            collection_article[0].save()
            print('已修改')
        else:
            # 不存在则创建
            CollectionArticle.objects.create(**item)


if __name__ == '__main__':
    urls = get_collection_urls()
    for url in urls:
        get_per_collection(url)

