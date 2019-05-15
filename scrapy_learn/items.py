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
    pass
