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
        self.file_name = "/re_" + (str(time.time()).replace(".", "")) + '.json'
        self.mail_file_name = "/mail_" + (str(time.time()).replace(".", "")) + '.json'
        self.f = None

        pass

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        if settings['CN_RESULT']:
            return cls(CN_RESULT=settings['CN_RESULT'])

    def process_item(self, item, spider):
        if spider.name == 'work':
            if item['mail'] == None:
                # 如果文件不存在--创建文件
                if item:
                    # 有内容才写
                    if not os._exists(self.result_root + self.file_name):
                        self.f = open(self.result_root + self.file_name, 'a')
                        self.f.write('[')
                        self.f.flush()
                        pass
                    # 转成字典类型--再转成json,中文处理-->最终转成字符串
                    context = json.dumps(dict(item), ensure_ascii=False).__str__() + ",\n"
                    self.f.write(context)
                    self.f.flush()
                    return item
            else:
                # mail反查

                pass

    def close_spider(self, spider):
        #文件存在才关闭
        if self.f:
            self.f.write(']')
            self.f.flush()
            self.f.close()
            # 删除结果中的空文件-和空信息的文件
            self.delete_file()

        pass

    def delete_file(self):
        # 删除结果文件中的空文件
        print("=========", self.result_root)
        if self.result_root:
            list = os.listdir(self.result_root)
            for i in range(0, len(list)):
                path = os.path.join(self.result_root, list[i])
                if os.path.isfile(path):
                    # 如果是文件--判断文件大小-如果为0就删除
                    # 如果文件大小为0
                    if os.path.getsize(path) == 0:
                        # 删除文件
                        if os.path.exists(path):
                            try:
                                os.remove(path)
                            except Exception as e:
                                print("出现异常", e)
                            print('=====>删除空白文件', path)
                    # 判断是否是空json
                    else:
                        with open(path, 'r', encoding='utf8') as f:
                            # 读取第一行
                            first_line = f.readline()
                            if first_line == '[]':
                                # 删除文件
                                if os.path.exists(path):
                                    try:
                                        os.remove(path)
                                    except Exception as e:
                                        print("出现异常", e)

                                    print('=====>删除空json文件', path)


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
