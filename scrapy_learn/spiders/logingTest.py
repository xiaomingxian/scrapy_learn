# -*- coding: utf-8 -*-
import scrapy
import logging

# 实例化logging
logger = logging.getLogger(__name__)


class BaiduSpiderSpider(scrapy.Spider):
    name = 'loging'
    allowed_domains = ['huaban.com']
    start_urls = ['https://huaban.com/']  # 开始爬取的位置

    # start_urls结果返回到parse
    def parse(self, response):
        logger.error('------------>error信息')
        logger.warning('---------->warning信息')
        logger.info('------------->info信息')
        logger.debug('------------>debug信息')
