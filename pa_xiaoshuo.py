# -*- coding: utf-8 -*-
# @Time    : 2020/6/21 11:09
# @Author  : banshaohuan
# @Site    :
# @File    : pa_xiaoshuo.py
# @Software: PyCharm
import requests
from lxml import etree
from fake_useragent import UserAgent

# 设置headers
ua = UserAgent()
headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh_CN,zh;q=0.9",
    "Connection": "close",
    "User-Agent": ua.random,
}

# 获取url链接的xml格式
def get_xml(url):
    res = requests.get(url, headers, timeout=10)
    res.encoding = res.apparent_encoding
    text = res.text
    xml = etree.HTML(text)
    return xml


# 获取文章内容
def get_content(xml, f):
    data = xml.xpath('//div[@class="readcontent"]/text()')
    for text in data:
        if text == "\n":
            pass
        else:
            f.write(text.replace("\n", ""))


def download_book(url):
    xml_list = get_xml(url)
    name = xml_list.xpath("//h1/text()")
    # 章节名
    chapters = xml_list.xpath('//div[@id="list-chapterAll"]//dd/a/text()')
    links = xml_list.xpath('//div[@id="list-chapterAll"]//dd/a/@href')

    print(f"《{name[0]}》获取中，共{len(links)}章")

    file_name = f"D:/{name[0]}.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        for i in range(0, len(links) - 200):
            f.write("\n")
            f.write(chapters[i])
            url_text = f"{url}{links[i]}"
            xml_content = get_xml(url_text)
            page = xml_content.xpath('//div[@class="book read"]//small/text()')
            get_content(xml_content, f)
            if "(1/2)" in page:
                url_text2 = f"{url_text[0:-5]}_2.html"
                xml_content2 = get_xml(url_text2)
                get_content(xml_content2, f)
            print(f"{chapters[i]}:已完成")
    print("下载完成")


if __name__ == "__main__":
    # url为小说目录页
    url = "https://www.oldtimescc.cc/go/16078/"
    download_book(url)
