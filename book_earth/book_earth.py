import requests
from lxml import etree
from fake_useragent import UserAgent
import pandas as pd
import time

# 设置headers
ua = UserAgent()
headers = {
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "zh_CN,zh;q=0.9",
    "Connection":"close",
    "User-Agent":ua.random
}

# 获取url链接的xml格式
def get_xml(url):
    res = requests.get(url,headers = headers, timeout=10)
    res.encoding = res.apparent_encoding
    text = res.text
    xml = etree.HTML(text)
    return xml

def get_content(xml):
    links = xml.xpath('//a[@rel="noreferrer nofollow"]/@href')
    texts = xml.xpath('//a[@rel="noreferrer nofollow"]/text()')
    return links, texts


if __name__ == "__main__":
    df_all = pd.DataFrame()
    url = "https://www.bookmarkearth.com/page?currentPage="
    for i in range(1, 118):
        xml = get_xml(url)
        links, texts = get_content(xml)
        df1 = pd.DataFrame({"link":links, "name": texts})
        df_all = df_all.append(df1)
        time.sleep(0.5)
    # df_all.to_csv('book_earth.csv', encoding='utf8')
    df_all.to_csv('book_earth1.csv', encoding='utf-8')
    # 设置encoding='utf_8_sig'能防止中文乱码
    df_all.to_csv('book_earth2.csv', encoding='utf_8_sig')
    df_all.to_csv('book_earth3.csv', encoding='gbk')