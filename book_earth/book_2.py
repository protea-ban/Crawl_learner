import requests
from lxml import etree
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
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
    res = requests.get(url,headers=headers, timeout=10)
    res.encoding = res.apparent_encoding
    text = res.text
    return text

def craw(url):
    html1 = get_xml(url)
    pat = r'<a href=".+?" rel="noreferrer nofollow" target="_blank">'
    match1 = re.compile(pat)
    result = re.findall(match1, html1)
    # pat2 = r'(?<=href=["]).*?(?=["])'
    # match2 = re.compile(pat2)
    # links_list = re.findall(match2, result)

    return result

if __name__ == '__main__':
    url = 'https://www.bookmarkearth.com/page?currentPage=1'
    res = craw(url)
    print(res)



# content = '''
# <a href="https://www.sjtiantang.com/" rel="noreferrer nofollow" target="_blank">
# <a href="http://www.tool77.com/" rel="noreferrer nofollow" target="_blank">
# <a href="https://www.xiaozhaolaila.com/" rel="noreferrer nofollow" target="_blank">
# '''
# match = re.compile(r'(?<=href=["]).*?(?=["])')
# # match = re.compile(r'[a-zA-z]+://[^\s]*')
# raw = re.findall(match,content)
# print(raw)