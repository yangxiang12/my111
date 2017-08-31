# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector,Selector
from scrapy.http import Request
import os
import requests
from concurrent.futures import ThreadPoolExecutor

class XhrSpider(scrapy.Spider):
    name = 'xhr'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://xiaohuar.com/hua/']
    photo = '../photo/'
    def parse(self, response):
        hxs = Selector(response=response)
        pool = ThreadPoolExecutor(10)
        #找标签，class是item masonry_brick
        user_list = hxs.xpath('//div[@class="item masonry_brick"]')
        # print(user_list)
        for item in user_list:
            price = item.xpath('.//span[@class="price"]/text()').extract_first()
            url = item.xpath('div[@class="item_t"]/div[@class="img"]//a//img/@src').extract_first()
            url2 = 'http://www.xiaohuar.com'+url
            # print(price,url)
            pool.submit(self.pho,url2,price)
        pool.shutdown()
        result = hxs.xpath('//a[re:test(@href,"http://www.xiaohuar.com/list-1-\d+.html")]/@href').extract()
        print(result)

        for url in result:
            yield Request(url=url,callback=self.parse)


    def pho(self,url,price):
        res = requests.get(url=url, )
        with open('%s%s.jpg' % (self.photo, price), 'wb') as f:
            f.write(res.content)