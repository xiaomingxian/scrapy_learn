# -*- coding: utf-8 -*-
import scrapy
import time
from pymysql import *


class BaiduSpiderSpider(scrapy.Spider):
    name = 'ip'
    allowed_domains = ['fanqieip.com']
    start_urls = [
        'https://www.fanqieip.com/free/China/2',
        'https://www.fanqieip.com/free/China/4',
        'https://www.fanqieip.com/free/China/5',
        'https://www.fanqieip.com/free/China/6',
        'https://www.fanqieip.com/free/China/7',
        'https://www.fanqieip.com/free/China/8',
        'https://www.fanqieip.com/free/China/9',
        'https://www.fanqieip.com/free/China/10',
        'https://www.fanqieip.com/free/China/11',
        'https://www.fanqieip.com/free/China/12',
        'https://www.fanqieip.com/free/China/13',
        'https://www.fanqieip.com/free/China/14',
        'https://www.fanqieip.com/free/China/15',
        'https://www.fanqieip.com/free/China/16',
        'https://www.fanqieip.com/free/China/17',
        'https://www.fanqieip.com/free/China/18',
        'https://www.fanqieip.com/free/China/19',
        'https://www.fanqieip.com/free/China/20',
        'https://www.fanqieip.com/free/China/21',

    ]  # 开始爬取的位置

    # start_urls结果返回到parse
    def parse(self, response):
        x = '//table[@class="layui-table"]/tbody/tr'
        res = response.xpath(x)
        # print(res.extract())
        for r in res:
            tds = r.xpath('./td')
            ip = str(tds[0].xpath('./div/text()')[0].extract())
            port = str((tds[1].xpath('./div/text()')[0].extract()))
            # print(ip,port)
            print('\'http://%s:%s\',' % (ip, port))
