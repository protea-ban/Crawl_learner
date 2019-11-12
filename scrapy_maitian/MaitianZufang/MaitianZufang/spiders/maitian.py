# -*- coding: utf-8 -*-
import scrapy
from MaitianZufang.items import MaitianzufangItem

class MaitianSpider(scrapy.Spider):
    name = 'maitian'
    # allowed_domains = ['http://bj.maitian.cn/zfall']
    start_urls = ['http://bj.maitian.cn/zfall/PG1']

    def parse(self, response):
        for item in response.xpath('//div[@class="list_title"]'):
            yield {
                'title': item.xpath('./h1/a/text()').extract_first().strip(),
                'price': item.xpath('./div[@class="the_price"]/ol/strong/span/text()').extract_first().strip(),
                'area': item.xpath('./p/span/text()').extract_first().replace('㎡', ''),
                'district': item.xpath('./p//text()').re(r'昌平|朝阳|东城|大兴|房山|丰台|海淀|门头沟|平谷|石景山|顺义|通州|西城')[0],
            }

        next_page_url = response.xpath('//div[@id="paging"]/a[@class="down_page"]/@href').extract_first()

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
