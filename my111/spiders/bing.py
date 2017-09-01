# -*- coding: utf-8 -*-
import scrapy


class BingSpider(scrapy.Spider):
    name = 'bing'
    allowed_domains = ['bing.com']
    start_urls = ['http://bing.com/']

    def parse(self, response):
        print(response.text)

