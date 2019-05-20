# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import os

logger = logging.getLogger(__name__)


class ProxytestSpider(scrapy.Spider):
    name = 'work'
    # allowed_domains = ['chinaz.com']
    start_urls = ['http://whois.chinaz.com/youdaody.info']
    base_url = 'http://whois.chinaz.com'
    mail_base_url = 'http://whois.chinaz.com/reverse?host=guo_xiao_qin@163.com&page='
    # 域名数组
    names = []
    # 数据源文件数组
    files = []
    # 数据源文件所在文件夹
    source_root = None
    # 解析结果所在文件夹
    result_root = None
    # 数据索引
    index = 0
    # 邮箱反查 页码
    mail_page = 1
    # 未查询到结果的文件--前缀加时间戳
    noResultFile = None

    # 初始化---
    def __init__(self, source_root, result_root):
        # 从配置文件读取配置的数据源所在文件
        self.source_root = source_root
        self.result_root = result_root
        # 递归查找所有文件进行便利
        list = os.listdir(self.source_root)
        for i in range(0, len(list)):
            path = os.path.join(self.source_root, list[i])
            if os.path.isfile(path):
                # 如果是文件---就读取文件---记录文件名[便于删除]
                self.files.append(path)
                with open(path, 'r', encoding='utf8') as f:
                    l_name = f.readlines()
                    for name in l_name:
                        # 排除空行
                        if name:
                            # 去除换行符
                            if '\n' in name:
                                self.names.append(name.replace('\n', ''))
                            else:
                                self.names.append(name)
        print('域名：', source_root, self.names)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        if settings['CN_SOURCE'] and settings['CN_SOURCE']:
            # 这里调用的是init()方法，，参数列表得保持一致
            return cls(source_root=settings['CN_SOURCE'], result_root=settings['CN_RESULT'])

    def parse(self, response):
        x_ = '//ul[@id="sh_info"]//li'
        res = response.xpath(x_)
        itim = {}
        for i in res:
            # 获取li下的div
            left = i.xpath('./div[@class="fl WhLeList-left"]')
            right = i.xpath('./div[@class="fr WhLeList-right"]')
            status = i.xpath('./div[@class="fr WhLeList-right clearfix"]')
            other = i.xpath('./div[@class="fr WhLeList-right block ball lh24"]')
            yuName = i.xpath('./div[@class="fl WhLeList-left h64"]')
            # //*[@id="sh_info"]/li[1]
            key = ''
            value = ''

            # 注册商，创建时间，过期时间，DNS
            if left and right:
                l = left.xpath('./text()').extract()
                r = right.xpath('./div/span/text()').extract()
                msg_l = []
                if l[0] == 'DNS':
                    r = right.xpath('./text()').extract()
                elif '时间' in l[0] or '域名服务器' in l[0]:
                    r = right.xpath('./span/text()').extract()
                # 长度判断
                if len(r) == 1:
                    r = r[0]
                    value = r
                else:
                    for m in r:
                        msg_l.append(m)
                        value = msg_l
                key = l[0]

            # 状态
            if left and status:
                l = left.xpath('./text()').extract()
                r = status.xpath('./p/span/text()').extract()
                msg = []
                if len(r) == 1:
                    r = r[0]
                    value = r
                else:
                    for m in r:
                        msg.append(m)
                        value = msg

                key = l[0]

            # 域名
            if yuName and right:
                l = yuName.xpath('./span/text()').extract()
                ys = right.xpath('./p/a')
                y_list = []
                for y in ys:
                    yuming = y.xpath('./text()').extract()[0]
                    if ('隐私') in yuming:
                        pass
                    elif ('反查') in yuming:
                        pass
                    else:
                        y_list.append(yuming)
                        value = y_list
                key = l[0]

            #    联系人，邮箱
            if left and other:
                l = left.xpath('./text()').extract()
                r = other.xpath('./span/text()').extract()
                if len(r) == 1:
                    r = r[0]
                key = l[0]
                if '邮箱' in key:
                    # 进行邮箱反查---构造url--进行请求
                    yield scrapy.Request(self.mail_base_url + str(self.mail_page), callback=self.mail_parse, dont_filter=True)

                    pass
                value = r
            if key == '' and value == '':
                pass
            else:
                itim[key] = value
        print('--->当前页码:', self.index, ',读取到的信息:', itim)
        # 初始url结果不传入管道
        if self.index != 0:
            if itim:
                yield itim
            else:
                # 记录未查询到结果的文件存在
                if self.noResultFile is None:
                    file_path = 'no_' + str(time.time()).replace('.', '') + '.txt'
                    self.noResultFile = open(file_path, 'a')
                else:
                    # 将域名填入 文件
                    self.noResultFile.write(self.names.index(self.index) + '\n')
                    self.noResultFile.flush()
                    self.noResultFile.close()
                # 未解析到结果---将域名放在未解决的文件
                print("--->未解析到结果，放入为解决文件", self.names.index(self.index))

        # 请求延时--避免反爬虫的  低级策略 Low!!!
        # time.sleep(3)
        # ==================================        解析结束        ===============================================
        # ==================================  构造下个请求--读取文件  ===============================================
        url = None
        if self.index < len(self.names):
            url = self.base_url + self.names[self.index]

        # 读取文件
        if len(self.names) == self.index + 1:
            print('--->读取完成')
        if self.index < len(self.names):
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
            self.index += 1
        else:
            self.delete_file()

    #  邮箱反查
    def mail_parse(self, response):



        pass

    def delete_file(self):
        # 所有数据爬取完毕-删除数据源-遍历files
        for file in self.files:
            print("---->删除文件：", file)
            if os.path.exists(file):
                os.remove(file)
