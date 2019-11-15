"""
爬取西刺代理网站上高匿可用IP，存储到Redis和TXT文件中
"""
import redis
import telnetlib
import urllib
from bs4 import BeautifulSoup

r = redis.Redis(host='127.0.0.1', port=6379)

for i in range(1, 3):
    xici_url = 'https://www.xicidaili.com/nn/{}'.format(i)
    req = urllib.request.Request(xici_url)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib.request.urlopen(req)
    html = response.read()

    bs_obj = BeautifulSoup(html, 'html.parser')

    for i in range(100):
        speed = float(bs_obj.select('td')[6+i * 10].div.get('title').replace('秒', ''))
        # 找出速度在0.2秒以内的
        if speed < 0.2:
            ip = bs_obj.select('td')[1 + i * 10].get_text()
            port = bs_obj.select('td')[2 + i * 10].get_text()
            ip_address = 'http://{}:{}'.format(ip, port)
            
            # 用telnet对IP进行验证
            try:
                telnetlib.Telnet(ip, port=port, timeout=2)
            except:
                print('Fail')
            else:
                print('success: ' + ip_address)
                # 写到Redis中
                r.sadd('ip_pool', ip_address)
                # 以追加的方式写到TXT文件中
                f = open('proxy_list.txt', 'a')
                f.write(ip_address + '\n')
                f.close()
