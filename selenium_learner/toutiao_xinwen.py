# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 15:11
# @Author  : banshaohuan
# @Site    : 
# @File    : toutiao_xinwen.py
# @Software: PyCharm
# 抓取头条新闻链接
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(chrome_options=option)
url = 'https://www.toutiao.com'

driver.get(url)
# print(driver.page_source)

timeout = 5
links = WebDriverWait(driver, timeout).until(
    lambda d: d.find_elements_by_xpath('//div[@ga_event="article_title_click"]/a')
)

for link in links:
    print(link.text)
    print(url+link.get_attribute('href'))
