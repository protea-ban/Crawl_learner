# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 20:54
# @Author  : banshaohuan
# @Site    :
# @File    : album_bilibili.py
# @Software: PyCharm
import os
import requests
import json
import time
from fake_useragent import UserAgent


def get_fake_agent():
    headers = {"User-Agent": UserAgent().random}

    return headers


# 获取图片链接
def get_urls(uid, page=0):
    # 存放图片链接
    pic_list = []
    while True:
        url = f"https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid={uid}&page_num={page}&page_size=30&biz=all"
        content = requests.get(url, headers=get_fake_agent(), verify=False).content

        time.sleep(2)

        dic = json.loads(content)
        if len(dic.get("data").get("items")) == 0:
            break
        # 返回的数据字典中图片信息在items中
        item_list = dic.get("data").get("items")
        for item in item_list:
            # item是图片链接
            item = item.get("pictures")[0].get("img_src")
            pic_list.append(item)

        page += 1
    return pic_list


# 保存图片到本地
def save_pic(pic_list, file_path="D:/Images"):
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    for i in range(len(pic_list)):
        content = requests.get(
            pic_list[i], headers=get_fake_agent(), verify=False
        ).content
        time.sleep(2)
        with open(f"{file_path}/{i+1}.{pic_list[i][-3:]}", "wb") as f:
            f.write(content)

        print(f"{i+1}.{pic_list[i][-3:]} is downloaded")


def main():
    # 不显示警告信息
    requests.packages.urllib3.disable_warnings()
    uid = 405576449
    pic_list = get_urls(uid)
    save_pic(pic_list)


if __name__ == "__main__":
    main()
