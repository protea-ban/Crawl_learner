# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 11:14
# @Author  : banshaohuan
# @Site    : 
# @File    : baidu_selenium.py
# @Software: PyCharm
# 用selenium模拟百度搜索python
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# chrome的配置
option = webdriver.ChromeOptions()
# 设置为headless，即不会出现浏览器
option.add_argument('headless')
# 启动时默认路径为Chrome.exe所在目录，将chromedriver放置该目录下即可不用添加路径参数
driver = webdriver.Chrome(chrome_options=option)
url = 'https://www.baidu.com'

# 打开网站
driver.get(url)

print(driver.title)

# 模拟在百度中搜索python
# 定位搜索框
timeout = 5
search_content = WebDriverWait(driver, timeout).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="kw"]'))
)
# 向找到的元素输入文本
search_content.send_keys('python')

time.sleep(3)

# 点击搜索
search_button = WebDriverWait(driver, timeout).until(
    lambda d:d.find_element_by_xpath('//input[@id="su"]')
)
search_button.click()

# 获取搜索结果
search_res = WebDriverWait(driver, timeout).until(
    lambda e: e.find_elements_by_xpath('//h3[contains(@class, "t")]/a[1]')
)

for item in search_res:
    print(item.text)

driver.close()
