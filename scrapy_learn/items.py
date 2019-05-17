# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyLearnItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义字段
    name = scrapy.Field()
    age = scrapy.Field()
    address = scrapy.Field()
    # ip和端口
    ip = scrapy.Field()
    port = scrapy.Field()
    # work
    zcs = scrapy.Field()
    c_time = scrapy.Field()
    g_time = scrapy.Field()
    dns = scrapy.Field()
    status = scrapy.Field()
    yum = scrapy.Field()
    people = scrapy.Field()
    mail = scrapy.Field()
    phone = scrapy.Field()



    pass
