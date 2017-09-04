# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector


class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['http://chouti.com/']
    cookie_dict = {}
    """
    1. 发送一个GET请求,抽屉
       获取cookie

    2. 用户密码POST登录：携带上一次cookie
       返回值：9999

    3. 为所欲为，携带cookie
	"""

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, callback=self.parse1)

    def parse1(self, response):
        # response.text 首页所有内容
        from scrapy.http.cookies import CookieJar
        cookie_jar = CookieJar()  # 对象，中封装了 cookies 解析cookie
        cookie_jar.extract_cookies(response, response.request)  # 去响应中获取cookies

        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        post_dict = {
            'phone': '8618614085772',
            'password': 'yang243667673',
            'oneMonth': 1,
        }
        #urllib解析出来请求头的格式
        import urllib.parse

        # 目的：发送POST进行登录
        yield Request(
            url="http://dig.chouti.com/login",
            method='POST',
            cookies=self.cookie_dict,
            body=urllib.parse.urlencode(post_dict),#'phone'='8618614085772'&'password'='yang243667673',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            callback=self.parse2
        )

    def parse2(self, response):
        print(response.text)
        # 获取新闻列表
        yield Request(url='http://dig.chouti.com/', cookies=self.cookie_dict, callback=self.parse3)

    def parse3(self, response):
        print(response.text)
        # 找div，class=part2, 获取share-linkid
        hxs = Selector(response)
        link_id_list = hxs.xpath('//div[@class="part2"]/@share-linkid').extract()
        print(link_id_list)
        for link_id in link_id_list:
            base_url = "http://dig.chouti.com/link/vote?linksId=%s" % (link_id,)
            yield Request(url=base_url, method="POST", cookies=self.cookie_dict, callback=self.parse4)

        page_list = hxs.xpath('//div[@id="dig_Lcpage"]//a/@href').extract()
        for page in page_list:
            # #http://dig.chouti.com/ /all/hot/recent/2
            page_url = "http://dig.chouti.com%s"%(page,)
            yield Request(url=page_url,callback=self.parse3)

    def parse4(self, response):
        print(response.text)