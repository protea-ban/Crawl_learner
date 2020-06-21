# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 18:24
# @Author  : banshaohuan
# @Site    :
# @File    : bizhi.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import os
import time
import random
from fake_useragent import UserAgent


index = "http://www.netbian.com/"
interval = 0.1
first_dir = "D:/彼岸桌面爬虫"
# 存放网站分类子页面的信息
classification_dict = {}

# 得到一个随机的header
def get_headers():
    # 设置headers
    ua = UserAgent()
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh_CN,zh;q=0.9",
        "Connection": "close",
        "User-Agent": ua.random,
    }

    return headers


# 获取页面筛选后的内容列表

# 获取页面筛选后的内容列表
def screen(url, select):
    headers = get_headers()
    html = requests.get(url=url, headers=headers)
    html.encoding = html.apparent_encoding
    html = html.text
    soup = BeautifulSoup(html, "lxml")
    return soup.select(select)


# 将分类子页面信息存放在字典中
def init_classification():
    url = index
    select = "#header > div.head > ul > li:nth-child(1) > div > a"
    classifications = screen(url, select)
    for c in classifications:
        href = c.get("href")
        text = c.string
        if text == "4K壁纸":  # 4K壁纸需要权限，无法爬取，只能跳过
            continue
        second_dir = f"{first_dir}/{text}"
        url = index + href
        global classification_dict
        classification_dict[text] = {"path": second_dir, "url": url}


# 获取页码
def screen_page(url, select):
    html = requests.get(url=url, headers=get_headers())
    html.encoding = html.apparent_encoding
    html = html.text
    soup = BeautifulSoup(html, "lxml")
    return soup.select(select)[0].next_sibling.text


def download(src, jpg_path):
    if isinstance(src, str):
        response = requests.get(src)
        while os.path.exists(jpg_path):
            jpg_path = f"{jpg_path.split('.')[0]}{random.randint(2,17)}.{jpg_path.split('.')[1]}"
        with open(jpg_path, "wb") as pic:
            for chunk in response.iter_content(128):
                pic.write(chunk)


# 定位到 1920 1080 分辨率图片
def handle_images(links, path):
    for link in links:
        href = link.get("href")
        # 过滤图片广告
        if href == "http://pic.netbian.com/":
            continue

        # 第一次跳转
        if "http://" in href:
            url = href
        else:
            url = index + href

        select = "div#main div.endpage div.pic div.pic-down a"
        link = screen(url, select)

        if link == []:
            print(f"{url}:无此图片，爬取失败")
            continue
        href = link[0].get("href")

        # 第二次跳转
        url = index + href

        # 找到要爬取的图片
        select = "div#main table a img"
        link = screen(url, select)
        if link == []:
            print(f"{url}:该图片需要登录才能爬取，爬取失败")
            continue
        # 这里去掉alt中所有的符号，只保留名字
        name = (
            link[0]
            .get("alt")
            .replace("\t", "")
            .replace("|", "")
            .replace(":", "")
            .replace("\\", "")
            .replace("/", "")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
        )
        print(name)  # 输出下载图片的文件名
        src = link[0].get("src")
        if requests.get(src).status_code == 404:
            print(f"{url}:该图片下载链接404， 爬取失败")
            print()
            continue
        print()
        jpg_path = f"{path}/{name}.jpg"
        if os.path.exists(jpg_path):
            continue
        download(src, jpg_path)
        time.sleep(interval)


def select_classification(choice):
    print("---------------------------")
    print("--------------" + choice + "-------------")
    print("---------------------------")
    second_url = classification_dict[choice]["url"]
    second_dir = classification_dict[choice]["path"]

    if not os.path.exists(second_dir):
        os.mkdir(second_dir)

    select = "#main > div.page > span.slh"
    page_index = screen_page(second_url, select)
    last_page_num = int(page_index)
    for i in range(0, last_page_num):
        if i == 0:
            url = second_url
        else:
            url = f"{second_url}index_{i+1}.htm"

        print(f"---------{choice}:{i+1}--------")

        path = f"{second_dir}/{i+1}"
        if not os.path.exists(path):
            os.mkdir(path)

        select = "div#main div.list ul li a"
        links = screen(url, select)
        handle_images(links, path)


# UI交互页面
def ui():
    print("-----------netbian----------")
    print("全部", end=" ")
    for c in classification_dict.keys():
        print(c, end=" ")
    print()
    choice = input("请输入分类名：")
    if choice == "全部":
        for c in classification_dict.keys():
            select_classification(c)
    elif choice not in classification_dict.keys():
        print("输入错误，请重新输入！")
        print("----")
        ui()
    else:
        select_classification(choice)


def main():
    if not os.path.exists(first_dir):
        os.mkdir(first_dir)
    init_classification()
    ui()


if __name__ == "__main__":
    main()
