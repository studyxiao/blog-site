import requests
import json
import time
from bs4 import BeautifulSoup
from PIL import Image
import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../blog'))  # 把包添加到系统目录
import pymysql
pymysql.install_as_MySQLdb()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temporal.settings')
import django
django.setup()

from mycollections.models import ZhiHuCategory, ZhiHuCollection

zhihu_url = 'https://www.zhihu.com'
zhihu_login_url = 'https://www.zhihu.com/login/email'  # 邮箱登录
zhihu_captcha_url = zhihu_url + '/captcha.gif'  # 验证码地址
zhihu_captcha_url_payload = {  # 验证码地址的参数
    'r': str(int(time.time() * 1000)),
    'type': 'login',
}
zhihu_profile_url = zhihu_url + '/settings/profile'  # 个人信息
zhihu_collection_url = zhihu_url + '/collection/%d'  # 收藏

headers = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'https://www.zhihu.com/',
    'Origin': 'https://www.zhihu.com',
    'Host': 'www.zhihu.com',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {
    'email': '',  # 用户邮箱
    'password': '',  # 密码
    'rememberme': 'true',
}

cookies_file_name = 'zhihu_cookies'  # 保存cookies的文件名
zhihu_login_captcha = 'zhihu_captcha.gif'  # 保存验证码的文件名

session = requests.Session()

session.headers.update(headers)


def login():
    """
    登录知乎,并保存cookies
    或者给session更新cookies.
    :return:
    """
    if os.path.exists(cookies_file_name):
        with open(cookies_file_name) as f:
            cookie = json.load(f)
        session.cookies.update(cookie)
    else:
        response = session.get(zhihu_url)
        soup = BeautifulSoup(response.text, 'lxml')
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
        data['_xsrf'] = xsrf
        with open(zhihu_login_captcha, 'wb') as f:
            captcha_resp = session.get(zhihu_captcha_url, params=zhihu_captcha_url_payload)
            f.write(captcha_resp.content)
        try:
            im = Image.open(zhihu_login_captcha)
            im.show()
        except:
            print('请打开下载的验证码%s' % zhihu_login_captcha)
        login_captcha = input('input captcha:\n').strip()
        data['captcha'] = login_captcha
        try:
            login_response = session.post(zhihu_login_url, data=data).json()
            if login_response['r'] == 0:
                print('登录成功')
                with open(cookies_file_name, 'w') as f:
                    json.dump(session.cookies.get_dict(), f)
                # os.remove(zhihu_login_captcha)
            else:
                print('登录失败')
        except:
            print('登录失败')


def get_collections():
    """
    获取收藏列表,
    并保存到数据库
    :return 收藏列表
    """
    collections_list = []
    content = session.get(zhihu_profile_url).content
    soup = BeautifulSoup(content, 'lxml')
    own_collections_url = 'https://www.' + soup.select('#js-url-preview')[0].text + '/collections'
    page_num = 0
    while True:
        page_num += 1
        url = own_collections_url + '?page=%d' % page_num
        # print(url)
        content = session.get(url).content
        soup = BeautifulSoup(content, 'lxml')
        datas = soup.select_one('#data').attrs['data-state']
        collections_dict_raw = json.loads(datas)['entities']['favlists'].values()
        if not collections_dict_raw:
            break
        for i in collections_dict_raw:
            name = i['title']
            category_url = zhihu_collection_url % i['id']
            item = {
                'name': name,
                'category_url': category_url,
            }
            collections_list.append(item)
            categories = ZhiHuCategory.objects.filter(category_url=category_url)
            if categories:
                # 存在则覆盖
                categories[0].name = name
                categories[0].category_url = category_url
                categories[0].save()
                print('已修改')
            else:
                # 不存在则创建
                category = ZhiHuCategory(name=name, category_url=category_url)
                category.save()

        print('=======收藏列表完成, 共 %d 个收藏夹======' % len(collections_list))
        return collections_list


def get_qa(collection_url):
    """
    获得一个收藏夹下的所有问题及答案,
    并且保存.
    :param collection_url:
    :return:
    """
    # 获得当前收藏夹在数据库中的条目
    category = ZhiHuCategory.objects.get(category_url=collection_url)
    page_num = 0
    while True:
        page_num += 1
        url = collection_url + '?page=%d' % page_num
        try:
            content = session.get(url).content
            soup = BeautifulSoup(content, 'lxml')
            titles = soup.select('.zm-item-title a')
            if len(titles) == 0:
                break
            votes = soup.select('.js-vote-count')  # .text
            answer_urls = soup.select('.toggle-expand')  # ['href']
            answers = soup.select('textarea')  # .text
            authors = soup.select('.author-link-line .author-link')  # .text ; ['href']
            for title, vote, answer_url, answer, author \
                    in zip(titles, votes, answer_urls, answers, authors):
                my_title = title.text  # 题目
                question_url = title['href']  # 问题地址
                if not question_url.startswith('http'):
                    question_url = zhihu_url + question_url
                answer_vote = vote.text  # 回答赞同数
                my_answer_url = answer_url['href']  # 回答地址
                if not my_answer_url.startswith('http'):
                    my_answer_url = zhihu_url + my_answer_url
                author_img = get_author_image(author['href'])  # 作者头像
                author_url = author['href']  # 作者地址
                if not author_url.startswith('http'):
                    author_url = zhihu_url + author_url

                answer_content = answer.text  # 回答内容
                # answer_content = re.compile(r'http//link\.zhihu\.com/\?target=').sub('', answer_content)
                answer_content = re.compile(r'[A-Za-z:]*//link\.zhihu\.com/\?target=').sub('', answer_content)

                # answer_content = answer_content.replace('//link.zhihu.com/?target=', '')
                answer_content = re.compile(r'data-rawwidth=\"\d+\"').sub('', answer_content)
                answer_content = re.compile(r'data-rawheight=\"\d+\"').sub('', answer_content)
                answer_content = re.compile(r' width=\"([7-9]\d{2}|[1-9]\d{3})\"').sub(r'', answer_content)
                answer_content = re.compile(r'target=\"_blank\"').sub('target="window', answer_content)
                answer_content = answer_content.replace('%3A', ':')
                answer_content = answer_content.replace('"', '\\"')
                answer_content = answer_content.replace("'", "\\'")
                item = {
                    'title': my_title,
                    'question_url': question_url,
                    'answer_vote': answer_vote,
                    'answer_url': my_answer_url,
                    'answer_content': answer_content,
                    'author': author.text,
                    'author_url': author_url,
                    'author_img': author_img,
                    'category': category,
                }
                articles = ZhiHuCollection.objects.filter(answer_url=my_answer_url)
                if articles:
                    # 存在则覆盖
                    articles[0].title = my_title
                    articles[0].question_url = question_url
                    articles[0].answer_vote = answer_vote
                    articles[0].answer_url = my_answer_url
                    articles[0].answer_content = answer_content
                    articles[0].author = author.text
                    articles[0].author_url = author_url
                    articles[0].author_img = author_img
                    articles[0].category = category
                    articles[0].save()
                    print('已修改')
                else:
                    # 不存在则创建
                    ZhiHuCollection.objects.create(**item)

        except:
            print('失败')
            pass


def get_author_image(author_url):
    """
    获得用户头像
    :param author_url: 作者短地址，e.g. /people/qinglan
    :return:
    """
    url = zhihu_url + author_url + '/answers'
    # print(url)
    try:
        content = session.get(url).content
        soup = BeautifulSoup(content, 'lxml')
        return soup.select_one('#ProfileHeader > div > div.ProfileHeader-wrapper '
                               '> div > div.UserAvatar.ProfileHeader-avatar > img')['src']
    except:
        return 'https://pic1.zhimg.com/da8e974dc_xl.jpg'

if __name__ == '__main__':
    login()
    collections = get_collections()
    for collection in collections:
        get_qa(collection['category_url'])
