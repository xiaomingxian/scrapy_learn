# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymysql
import json

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
            return item  # 告诉引擎-已经处理完毕


class TestPipeline(object):
    def process_item(self, item, spider):
        print("%s" % "优先级测试")
        return item


class ipPipleLine(object):
    # 初始化的时候只执行一次
    def __init__(self):
        # self.f = open(r"C:\xxm\learn\python_workspace\scrapy_learn/file/ip.txt", 'w', encoding='utf8')
        self.f = open(r"/Users/xxm/develop/py_workspace/scrapy_learn/file/ip.txt", 'w', encoding='utf8')
        pass

    def process_item(self, item, spider):
        if spider.name == 'ipSpider':
            # content = json.dumps(dict(item), ensure_ascii=False)  # 默认是ascii false后为unicode
            # c = content.encode('utf8')
            #
            # print('----->pipeline:', c)
            print("ip----", item['ip'])
            print("port----", item['port'])
            return item

    def close_spider(self, spider):
        # 爬取完后执行
        self.f.close()
        pass


class workPipleLine(object):
    # 初始化的时候只执行一次
    def __init__(self):
        self.f = open("work.txt", 'w')
        pass

    def process_item(self, item, spider):
        if spider.name == 'work':
            # 转成字典类型--再转成json,中文处理-->最终转成字符串
            context = json.dumps(dict(item), ensure_ascii=False).__str__() + "\n"
            self.f.write(context)

            return item

    def close_spider(self,spider):
        self.f.close()
        pass


class cnPipleLine(object):
    pass
    # 初始化的时候只执行一次
    # def __init__(self):
    #     self.f = open("/Users/xxm/develop/py_workspace/scrapy_learn/file/names", 'w')
    #     pass
    #
    # def process_item(self, item, spider):
    #     if spider.name == 'cn_work':
    #         # 转成字典类型--再转成json,中文处理-->最终转成字符串
    #         self.f.write(item['cn']+'\n')
    #
    #         return item
    #
    # def close_spider(self,spider):
    #     self.f.close()
    #     pass
