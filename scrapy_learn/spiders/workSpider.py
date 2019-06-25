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
    # ---------------------------- 跟目录--------------------------
    # 域名数据源文件所在文件夹
    source_root = None
    # 解析结果所在文件夹
    result_root = None
    # 邮箱反查失败根目录
    mail_froot = None
    # --------------------------域名数组-----------------------------
    # 域名集合
    names = []
    # 数据源文件数组
    files = []
    # 未查询到结果的文件--前缀加时间戳
    noResultFile = None
    #  ----------------------------邮箱反查--------------------------------
    mail_base_url = 'http://whois.chinaz.com/reverse?host='
    # ----------分页查询
    # 失败的请求地址集合
    mail_url_fail = []
    # 邮件文件集合
    fmfiles = []
    # 未查询到结果的文件
    noResultMF = None
    # 延迟配置
    cn_delay = None
    mail_delay = None

    # 初始化---
    def __init__(self, source_root, result_root, mail_path, cn_d, mail_d):
        # 从配置文件读取配置的数据源所在文件
        self.source_root = source_root
        self.result_root = result_root
        self.mail_froot = mail_path
        self.cn_delay = cn_d
        self.mail_delay = mail_d
        # 递归查找所有文件进行便利
        self.searchUrls(self.names, self.source_root, self.files)
        self.searchUrls(self.mail_url_fail, self.mail_froot, self.fmfiles)
        # 装载完毕后直接删除
        self.delete_file(self.files)
        self.delete_file(self.fmfiles)

        # print('域名：', self.names)
        # print('fmail：', self.mail_url_fail)
        # 递归查找所有失败邮箱反查地址

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        if settings['CN_SOURCE'] and settings['CN_SOURCE'] and settings['MAIL_FAIL']:
            # 这里调用的是init()方法，，参数列表得保持一致
            return cls(source_root=settings['CN_SOURCE'], result_root=settings['CN_RESULT'],
                       mail_path=settings['MAIL_FAIL'], cn_d=settings['CN_DELAY'], mail_d=settings['MAIL_DELAY'])

    def parse(self, response):
        # 放慢爬取速度
        if self.cn_delay:
            time.sleep(int(self.cn_delay))
        # 初始url不解析
        currentUrl = str(response.request.url)
        if currentUrl != self.start_urls[0]:
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
                    if '邮箱' in key and r != '':
                        # 直接构造5个页码---校验放在回调函数去做
                        for page in range(1, 6):
                            mailurl = self.mail_base_url + r + '&page=' + str(page)
                            yield scrapy.Request(mailurl, callback=self.mail_parse, dont_filter=True)
                    value = r
                if key == '' and value == '':
                    pass
                else:
                    itim[key] = value
            print('--->域名反查:读取到的信息:', itim)
            # 初始url结果不传入管道
            if currentUrl != self.start_urls[0]:
                if itim != {}:
                    itim['type'] = 'cn'
                    yield itim
                else:
                    # 文件不存在先创建文件
                    if self.noResultFile == None:
                        file_path = self.source_root + '/no_' + str(time.time()).replace('.', '') + '.txt'
                        self.noResultFile = open(file_path, 'a')
                    # 将失败名吸入文件
                    # http://whois.chinaz.com/xxx
                    self.noResultFile.write(currentUrl.split('whois.chinaz.com')[1] + '\n')
                    self.noResultFile.flush()

        # ==================================  构造下个请求[域名]--读取文件  ===============================================
        for cn_url in self.names:
            url = self.base_url + cn_url
            self.names.remove(cn_url)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

        # ==================================  构造下个请求[邮箱]--读取文件  ===============================================
        for mUrl in self.mail_url_fail:
            url = mUrl
            self.mail_url_fail.remove(mUrl)
            yield scrapy.Request(url, callback=self.mail_parse, dont_filter=True)

    #  邮箱反查----仅解析
    def mail_parse(self, response):
        # 放慢爬取速度
        if self.mail_delay:
            time.sleep(int(self.mail_delay))
        # 请求异常所在位置
        currentUrl = str(response.request.url)
        # print('请求地址：', currentUrl)
        # 请求是否成功判断
        ex_page = '//*[@id="ajaxInfo"]/ul/li[@class="tc ptb10 col-red YaHei fz14"]'
        ex_path = '//*[@id="ajaxInfo"]/ul/div' + '[@class="tc ptb10 col-red YaHei fz14"]/text()'
        print('-------====================邮箱-错误校验--被反爬虫:', len(response.xpath(ex_path).extract()), '--页码错误:',
              len(response.xpath(ex_page).extract()))
        if response.status != 200 or (len(response.xpath(ex_path).extract()) != 0) or (
                len(response.xpath(ex_page).extract()) != 0):

            # 存入失败文件夹
            if len(response.xpath(ex_page).extract()) != 0:
                print('---------------->邮箱页码错误 忽略.......')
                # 如果存储的邮箱页码是错误的 -- 不再进行错误存储
                pass
            else:
                print('---------------->邮箱-解析到的邮箱数据 请求失败--直接存入失败文件.......')
                if self.noResultMF == None:
                    file = self.mail_froot + '/m_' + str(time.time()).replace('.', '') + '.txt'
                    self.noResultMF = open(file, 'a')
                # 将邮箱地址填入 文件
                self.noResultMF.write(currentUrl + '\n')
                self.noResultMF.flush()
        else:
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

                if itim != {}:
                    itim['type'] = 'mail'
                    itim['mail'] = self.mailName(currentUrl)
                    # print('-------------->邮箱反查信息:', itim)
                    yield itim

    # 删除文件方法抽取
    def delete_file(self, root):
        # 所有数据爬取完毕-删除数据源-遍历files
        for file in root:
            print("---->删除文件：", file)
            if os.path.exists(file):
                os.remove(file)

    # 邮箱名称获取
    def mailName(self, currentUrl):
        hostName = None
        if '&' in currentUrl:
            hostName = currentUrl.split('?')[1].split('&')[0].split('=')[1]
        else:
            hostName = currentUrl.split('=')[1]
        return hostName

    def searchUrls(self, rongqi, root, delfile):
        list = os.listdir(root)
        for i in range(0, len(list)):
            path = os.path.join(root, list[i])
            if os.path.isfile(path):
                # 如果是文件---就读取文件---记录文件名[便于删除]
                delfile.append(path)
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
