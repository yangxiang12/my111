# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector


class ChouTiSpider(scrapy.Spider):
    # 爬虫应用的名称，通过此名称启动爬虫命令
    name = "chouti"
    # 允许的域名
    allowed_domains = ["chouti.com"]
    start_url = ['http://chouti.com/']
    cookies_dict = {}
    """
    1.发送一个GET请求，抽屉
        获取cookies
    2.用户密码POST登录：携带上一次cookie
        返回值：9999

    3.为所欲为：携带cookie
    """

    def start_requests(self):
        for url in self.start_url:
            #dont_filter:过滤，
            yield Request(url,dont_filter=True,callback=self.parse1)

    def parse1(self,response):
        #response.text首页所有内容
        from scrapy.http.cookies import CookieJar
        cookie_jar = CookieJar()#对象中封装了cookies
        cookie_jar.extract_cookies(response,response.request)#去响应中获取cookies

        for k,v in cookie_jar._cookies.items():
            for i,j in v.items():
                for m,n in j.items():
                    self.cookies_dict[m] = n.value

        post_dict = {
            'phone':'8618614085772',
            'password':'yang243667673',
            'oneMonth':1,
        }
        import urllib.parse

        #目的：发送POST进行登录
        yield  Request(
            url="http://dig.chouti.com/login",
            method="POST",
            cookies=self.cookies_dict,
            body=urllib.parse.urlencode(post_dict),#将字典转换成phone=8618614085772&password=yang243667673
            headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'},
            callback=self.parse2
        )

    def parse2(self, response):
        print(response.text)
        print('......')
        #获取新闻列表
        yield Request(url='http://dig.chouti.com/',cookies=self.cookies_dict,callback=self.parse3)

    def parse3(self, response):
        #找到div,class=part2,获取share-Linkid
        print('parse3...')
        print(response.text)
        hxs = Selector(response)
        link_id_list = hxs.xpath('//div[@class="part2"]/@share-Linkid').extract()
        print(link_id_list)
        for link_id in link_id_list:
            base_url = "http://dig.chouti.com/link/vote?linksId=%s"%link_id
            yield Request(url=base_url,method='POST',cookies=self.cookies_dict,callback=self.parse4)

    def parse4(self, response):
        print(response.text)
        print(response)
