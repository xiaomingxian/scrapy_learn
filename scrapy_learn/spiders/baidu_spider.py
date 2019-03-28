# -*- coding: utf-8 -*-
import scrapy


class BaiduSpiderSpider(scrapy.Spider):
    name = 'baidu_spider'
    allowed_domains = ['baidu.com']
    start_urls = ['https://movie.douban.com/']  # 开始爬取的位置

    # start_urls结果返回到parse
    def parse(self, response):
        # xpath解析
        print(response)
        pass
