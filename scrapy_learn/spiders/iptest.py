# -*- coding: utf-8 -*-
import scrapy


class IptestSpider(scrapy.Spider):
    name = 'iptest'
    # allowed_domains = ['chinaz.com']

    def start_requests(self):
        url = 'http://ip.chinaz.com/getip.aspx'

        for i in range(4):
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('--->ip代理测试：',response.text)
        pass
