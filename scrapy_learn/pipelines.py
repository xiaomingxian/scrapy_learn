# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 数据可以在多个pipline中传递

class ScrapyLearnPipeline(object):
    # 此方法不可改名-----区分多个spider   spider.name
    def process_item(self, item, spider):
        if spider.name == 'huaban':
            print('===>', item)
            return item


class TestPipeline(object):
    def process_item(self, item, spider):
        print("%s" % "优先级测试")
        return item
