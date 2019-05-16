# -*- coding: utf-8 -*-
import scrapy


class ProxytestSpider(scrapy.Spider):
    name = 'proxytest'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/']

    def parse(self, response):
        url_xpath = '//@href'
        res = response.xpath(url_xpath)
        for i in res:
            print(str(i.extract()))

        pass
