# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
 
 
class DigSpider(scrapy.Spider):
    # 爬虫应用的名称，通过此名称启动爬虫命令
    name = "dig"
 
    # 允许的域名
    allowed_domains = ["chouti.com"]
 
    # 起始URL
    start_urls = [
        'http://dig.chouti.com/',
    ]
 
    has_request_set = {}
 
    def parse(self, response):
        print(response.url)
 
        hxs = HtmlXPathSelector(response)
        page_list = hxs.select('//div[@id="dig_lcpage"]//a[re:test(@href, "/all/hot/recent/\d+")]/@href').extract()
        for page in page_list:
            page_url = 'http://dig.chouti.com%s' % page
            key = self.md5(page_url)
            if key in self.has_request_set:
                pass
            else:
                self.has_request_set[key] = page_url
                obj = Request(url=page_url, method='GET', callback=self.parse)
                yield obj
 
    @staticmethod
    def md5(val):
        import hashlib
        ha = hashlib.md5()
        ha.update(bytes(val, encoding='utf-8'))
        key = ha.hexdigest()
        return key