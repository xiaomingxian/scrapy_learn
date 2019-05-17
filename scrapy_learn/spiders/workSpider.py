# -*- coding: utf-8 -*-
import scrapy
import logging
logger = logging.getLogger(__name__)

class ProxytestSpider(scrapy.Spider):
    name = 'work'
    # allowed_domains = ['chinaz.com']
    start_urls = ['http://whois.chinaz.com/youdaody.info']
    base_url='http://whois.chinaz.com'
    names = []
    file_path = r'/Users/xxm/develop/py_workspace/scrapy_learn/file/names'
    index = 0

    def __init__(self):
        with open(self.file_path, 'r', encoding='utf8') as f:
            l_name = f.readlines()
            for name in l_name:
                if '\n' in name:
                    self.names.append(name.replace('\n',''))
                else:
                    self.names.append(name)
            print(self.names)
            print(len(self.names))

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
                value = r
            if key == '' and value == '':
                pass
            else:
                itim[key] = value
        # logger.info('--->当前页码{},读取到的信息{}',self.index,itim)
        print('--->当前页码:',self.index,',读取到的信息:',itim)
        if self.index!=0:
            yield itim

        # 构造下个请求--读取文件
        url=None
        if self.index<len(self.names):
            url =self.base_url+ self.names[self.index]

        # print("----域名个数：",len(self.names))
        # 读取文件
        if len(self.names) == self.index+1:
            print('--->读取完成')
        if self.index < len(self.names):
            yield scrapy.Request(url, callback=self.parse,dont_filter=True)

            self.index += 1



