# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 16:18
# @Author  : banshaohuan
# @Site    :
# @File    : jiandan.py
# @Software: PyCharm
import re
import urllib.request
from http import cookiejar

headers = {
    "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": " gb2312,utf-8",
    "Accept-Language": " zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
    "Connection": "keep-alive",
    "referer": "qq.com",
}
cjar = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
headall = []

for key, value in headers.items():
    item = (key, value)
    headall.append(item)

opener.addheaders = headall
urllib.request.install_opener(opener)


def craw(url, page):
    html1 = urllib.request.urlopen(url).read()
    html1 = str(html1)

    pat1 = '<ul id="pins">.+?</ul>'
    result1 = re.compile(pat1, re.S).findall(html1)
    result1 = result1[0]
    pat2 = "data-original=\\\\\\'(.*?)\\\\\\'"
    image_list = re.compile(pat2, re.S).findall(result1)

    index = 1
    path_name = "D:/Images/jiandan/xinggan/"
    import os

    if not os.path.exists(path_name):
        os.mkdir(path_name)
    for image_url in image_list:
        file_name = path_name + str(page) + "_" + str(index) + ".jpg"
        try:
            urllib.request.urlretrieve(image_url, filename=file_name)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                index += 1
            if hasattr(e, "reason"):
                index += 1

        index += 1


for i in range(1, 10):
    url = "http://www.mzitu.com/xinggan/page/" + str(i)
    import time

    time.sleep(6)
    print(url)
    craw(url, i)
