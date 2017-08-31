# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http.cookies import CookieJar
from scrapy import FormRequest


class ChouTiSpider(scrapy.Spider):
    # 爬虫应用的名称，通过此名称启动爬虫命令
    name = "chouti"
    # 允许的域名
    allowed_domains = ["chouti.com"]

    cookie_dict = {}
    has_request_set = {}

    def start_requests(self):
        url = 'http://dig.chouti.com/'
        # return [Request(url=url, callback=self.login)]
        yield Request(url=url, callback=self.login)

    def login(self, response):
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)
        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        req = Request(
            url='http://dig.chouti.com/login',
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            body='phone=8618614085772&password=yang243667673&oneMonth=1',
            cookies=self.cookie_dict,
            callback=self.check_login
        )
        yield req

    def check_login(self, response):
        req = Request(
            url='http://dig.chouti.com/',
            method='GET',
            callback=self.show,
            cookies=self.cookie_dict,
            dont_filter=True
        )
        yield req

    def show(self, response):
        # print(response)
        hxs = HtmlXPathSelector(response)
        news_list = hxs.select('//div[@id="content-list"]/div[@class="item"]')
        for new in news_list:
            # temp = new.xpath('div/div[@class="part2"]/@share-linkid').extract()
            link_id = new.xpath('*/div[@class="part2"]/@share-linkid').extract_first()
            yield Request(
                url='http://dig.chouti.com/link/vote?linksId=%s' %(link_id,),
                method='POST',
                cookies=self.cookie_dict,
                callback=self.do_favor
            )

        page_list = hxs.select('//div[@id="dig_lcpage"]//a[re:test(@href, "/all/hot/recent/\d+")]/@href').extract()
        for page in page_list:

            page_url = 'http://dig.chouti.com%s' % page
            import hashlib
            hash = hashlib.md5()
            hash.update(bytes(page_url,encoding='utf-8'))
            key = hash.hexdigest()
            if key in self.has_request_set:
                pass
            else:
                self.has_request_set[key] = page_url
                yield Request(
                    url=page_url,
                    method='GET',
                    callback=self.show
                )

    def do_favor(self, response):
        print(response.text)
