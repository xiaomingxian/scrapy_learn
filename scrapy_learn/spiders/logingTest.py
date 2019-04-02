# -*- coding: utf-8 -*-
import scrapy
import logging



class BaiduSpiderSpider(scrapy.Spider):
    name = 'loging'
    allowed_domains = ['huaban.com']
    start_urls = ['https://huaban.com/']  # 开始爬取的位置

    # start_urls结果返回到parse
    def parse(self, response):
        logging.error('------------>error信息')
        logging.warning('---------->warning信息')
        logging.info('------------->info信息')
        logging.debug('------------>debug信息')
