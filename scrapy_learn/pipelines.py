# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymysql
import json
import time
import os

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


#
class ipPipleLine(object):
    # 初始化的时候只执行一次
    def __init__(self):
        self.f = open(r"C:\xxm\learn\python_workspace\scrapy_learn/file/ip.txt", 'w', encoding='utf8')
        # self.f = open(r"/Users/xxm/develop/py_workspace/scrapy_learn/file/ip.txt", 'w', encoding='utf8')
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


# 没执行一次爬虫命令就创建一个文件
class workPipleLine(object):
    # 初始化的时候只执行一次
    def __init__(self, CN_RESULT):
        self.result_root = CN_RESULT
        self.file_name = "/yu_" + (str(time.time()).replace(".", "")) + '.json'
        self.mail_file_name = "/mail_" + (str(time.time()).replace(".", "")) + '.json'
        self.yf = None
        self.mf = None

        pass

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        if settings['CN_RESULT']:
            return cls(CN_RESULT=settings['CN_RESULT'])

    def process_item(self, item, spider):
        if spider.name == 'work':
            if item['type'] == 'cn':
                fileName = self.result_root + self.file_name
                if self.yf == None:
                    self.yf = open(fileName, 'a')
                    self.yf.write('[\n')
                    self.yf.flush()
                self.writeContext(item, self.yf)
            elif item['type'] == 'mail':
                fileName = self.result_root + self.mail_file_name
                if self.mf == None:
                    self.mf = open(fileName, 'a')
                    self.mf.write('[\n')
                    self.mf.flush()

                self.writeContext(item, self.mf)

    def writeContext(self, item, file):
        # 转成字典类型--再转成json,中文处理-->最终转成字符串
        context = json.dumps(dict(item), ensure_ascii=False).__str__() + "\n,\n"
        file.write(context)
        file.flush()
        return item

    def close_spider(self, spider):
        # 读取最后一行删除逗号
        # 文件存在才关闭
        # 域名文件
        if self.yf != None:
            self.yf.close()
            lines=[]
            with open(str(self.yf.name),'r') as f:
                lines = f.readlines()
                lines[len(lines) - 1] = ']'
            with open(str(self.yf.name),'w') as f:
                f.writelines(lines)
                f.flush()
                f.close()
        # 邮箱文件
        if self.mf != None:
            self.mf.close()
            lines = []
            with open(str(self.mf.name), 'r') as f:
                lines = f.readlines()
                lines[len(lines) - 1] = ']'
            with open(str(self.mf.name), 'w') as f:
                f.writelines(lines)
                f.flush()
                f.close()
        print("=====>结果文件写入完成")


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
