# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 15:25
# @Author  : banshaohuan
# @Site    : 
# @File    : sougou_weixin.py
# @Software: PyCharm
# 利用搜狗搜索接口抓取微信公众号

import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

option = webdriver.ChromeOptions()
# option.add_argument('headless')

driver = webdriver.Chrome(chrome_options=option)
url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=python_shequ'

driver.get(url)

timeout = 5
link = WebDriverWait(driver, timeout).until(lambda d: d.find_element_by_link_text('Python爱好者社区'))

link.click()

time.sleep(1)
# 切换页面
windows_handles = driver.window_handles
driver.switch_to.window(windows_handles[-1])
print(driver.title)
