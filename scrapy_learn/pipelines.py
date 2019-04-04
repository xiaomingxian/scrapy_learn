# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymysql

client = MongoClient('localhost', 27017)
db = client['scrapy_db']
table = db['huaban_table']


# 数据可以在多个pipline中传递

class ScrapyLearnPipeline(object):
    # 此方法不可改名-----区分多个spider   spider.name
    def process_item(self, item, spider):
        if spider.name == 'huaban':
            print('===>', item)
            try:
                table.insert(item)

            except Exception as e:
                print(e)
            print("----->", table.find())
            print('存储成功')
            return item


class TestPipeline(object):
    def process_item(self, item, spider):
        print("%s" % "优先级测试")
        return item
