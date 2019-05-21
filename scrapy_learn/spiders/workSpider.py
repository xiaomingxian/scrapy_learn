# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import os
import re

logger = logging.getLogger(__name__)


class ProxytestSpider(scrapy.Spider):
    name = 'work'
    # allowed_domains = ['chinaz.com']
    start_urls = ['http://whois.chinaz.com/youdaody.info']
    base_url = 'http://whois.chinaz.com'
    mail_base_url = 'http://whois.chinaz.com/reverse?host='
    # 域名数组------------------------------------------------------------
    names = []
    # 数据源文件数组
    files = []
    # 数据源文件所在文件夹
    source_root = None
    # 解析结果所在文件夹
    result_root = None
    # 数据索引
    index = 0
    # 未查询到结果的文件--前缀加时间戳
    noResultFile = None
    # 邮箱反查 ------------------------------------------------------------
    # 页码
    mail_page = 1
    # 总页码
    mail_total = None
    # 失败地址的根目录
    mail_froot=None
    # 失败的请求地址
    mail_url_fail = []

    # 初始化---
    def __init__(self, source_root, result_root, mail_path):
        # 从配置文件读取配置的数据源所在文件
        self.source_root = source_root
        self.result_root = result_root
        self.mail_froot=mail_path
        # 递归查找所有文件进行便利
        self.searchUrls(self.names,self.source_root)
        self.searchUrls(self.mail_url_fail,self.mail_froot)

        print('域名：', source_root, self.names)
        print('fmail：', source_root, self.names)
        #递归查找所有失败邮箱反查地址


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        if settings['CN_SOURCE'] and settings['CN_SOURCE'] and settings['MAIL_FAIL']:
            # 这里调用的是init()方法，，参数列表得保持一致
            return cls(source_root=settings['CN_SOURCE'], result_root=settings['CN_RESULT'],
                       mail_path=settings['MAIL_FAIL'])

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
                if len(r) >= 1:
                    r = r[0]
                else:
                    r = ''
                key = l[0]
                # 此处邮箱查询应 过滤掉 first_url
                # and self.index != 0
                if '邮箱' in key and r != '':
                    # 先查总页数
                    # 进行邮箱反查---构造url--进行请求
                    mailurl = self.mail_base_url + r + '&page=1'
                    yield scrapy.Request(mailurl, callback=self.mail_parse, dont_filter=True)

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
                itim['type'] = 'cn'
                yield itim
            else:
                # 文件不存在先创建文件
                if self.noResultFile == None:
                    file_path = self.source_root + '/no_' + str(time.time()).replace('.', '') + '.txt'
                    self.noResultFile = open(file_path, 'a')

                # 将域名填入 文件
                if self.index < len(self.names):
                    self.noResultFile.write(self.names[self.index] + '\n')
                    self.noResultFile.flush()
                    # self.noResultFile.close()
                pass

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
        # 请求异常所在位置
        currentUrl = str(response.request.url)
        print('请求地址：', currentUrl)
        ex_path = '//*[@id="ajaxInfo"]/ul/div' + '[@class="tc ptb10 col-red YaHei fz14"]/text()'
        if response.status != 200 or (len(response.xpath(ex_path).extract()) != 0):
            print('异常出现--再次尝试此地址')
            yield scrapy.Request(currentUrl, callback=self.mail_parse, dont_filter=True)

        else:

            hostName = None
            if '&' in currentUrl:
                hostName = currentUrl.split('?')[1].split('&')[0].split('=')[1]
                pass
            else:
                hostName = currentUrl.split('=')[1]
                pass

            # 总页数----构造分页
            total_p = '//*[@id="pagelist"]/span[@class="col-gray02"]/text()'
            pstr = response.xpath(total_p).extract()[0]
            p = int(re.findall('\d+', pstr)[0])

            # 总页数赋过值 就不再赋值----个别数据量过大只爬 100 条
            if self.mail_total == None:
                if p <= 5:
                    self.mail_total = p
                else:
                    self.mail_total = 5
            # ---------------------------------------------- 页码解析完毕  --------------------------------------------------
            # 所有li标签
            allLi = '//*[@id="ajaxInfo"]/ul/li'
            # 符合条件的li标签---多条件 | 隔开
            m_xpah = allLi + '[@class="WhoListCent Wholist clearfix bor-b1s02"] |' + allLi + '[@class="WhoListCent Wholist clearfix bor-b1s02 bg-list"]'
            res = response.xpath(m_xpah)
            itim = {}
            for i in res:
                # 域名 xpath
                yuMing = './div[@class="w13-0 domain"]/div/a/@href'
                # 注册人 xpath
                regPer = './div[@class="w13-0 man"]/div/text()'
                phone = './div[@class="w13-0 phone"]/a/text()'
                # 注册商
                trader = './div[@class="w13-0 trader"]/div/text()'
                # dns
                DNS = './div[@class="w13-0 dns"]/div/p/text()'
                # 注册时间
                regTim = './div[@class="w90"]/text()'

                domain = i.xpath(yuMing).extract()
                man = i.xpath(regPer).extract()
                phone = i.xpath(phone).extract()
                trader = i.xpath(trader).extract()
                DNS = i.xpath(DNS).extract()
                regTim = i.xpath(regTim).extract()

                if domain:
                    itim['domain'] = domain[0]

                if man:
                    itim['man'] = man[0]

                if phone:
                    itim['phone'] = phone[0]

                if trader:
                    itim['trader'] = trader[0]

                if DNS:
                    itim['DNS'] = DNS
                if regTim:
                    itim['startTime'] = regTim[0]

                if regTim[1]:
                    itim['exceedTime'] = regTim[1]

                if itim:
                    itim['type'] = 'mail'
                # print('-------------->邮箱反查信息:', itim)
                yield itim
            # 构造下一个请求
            if self.mail_page < self.mail_total:
                self.mail_page += 1
                next_url = self.mail_base_url + hostName + '&page=' + str(self.mail_page)
                yield scrapy.Request(next_url, callback=self.mail_parse, dont_filter=True)
            else:
                # 结束循环 索引归为
                self.mail_page = 1,
                return
                pass

    def delete_file(self):
        # 所有数据爬取完毕-删除数据源-遍历files
        for file in self.files:
            print("---->删除文件：", file)
            if os.path.exists(file):
                os.remove(file)

    def searchUrls(self,rongqi,root):
        list = os.listdir(root)
        for i in range(0, len(list)):
            path = os.path.join(root, list[i])
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
                                rongqi.append(name.replace('\n', ''))
                            else:
                                rongqi.append(name)
