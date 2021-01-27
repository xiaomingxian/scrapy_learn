# -*- coding: utf-8 -*-
import scrapy
import time
from pymysql import *

con = connect(host='49.234.25.12', port=3306, user='root', passwd='Mysql_root_123456', db='landchina', charset='utf8')
cur = con.cursor()


class BaiduSpiderSpider(scrapy.Spider):
    name = 'lc'
    allowed_domains = ['landchina.com']
    start_urls = [
        'https://www.landchina.com/default.aspx?tabid=263&ComName=default']  # 开始爬取的位置
    totalPage = None
    currentPage = 1
    totalData = 0

    # 第二个请求
    secUrl = 'https://www.landchina.com/default.aspx?tabid=386&comname=default&'

    def start_requests(self):
        self.totalData = None
        self.currentPage = 1
        self.totalData = 0
        print('----------------')
        yield scrapy.FormRequest(
            url='https://www.landchina.com/default.aspx?tabid=263&ComName=default',
            formdata={
                'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                'TAB_QuerySubmitConditionData': '9f2c3acd-0256-4da2-a659-6949c4671a2a:2015-1-1~',  # 开始日期
                'TAB_QuerySubmitPagerData': '1'  # 开始页码
            },
            callback=self.parse
        )

    # start_urls结果返回到parse
    def parse(self, response):

        xpath_url = '//*[@id="TAB_contentTable"]/tbody/tr'
        res = response.xpath(xpath_url)
        if self.totalPage == None:
            # 首次进来 把总数量查出来
            page_xpath = '//td[@class="pager"]'
            p = response.xpath(page_xpath)[0].xpath('./text()').extract()[0]
            tpage = p.split('页')[0].split('共')[1]
            print('---初次查 记录总数', self.totalPage)
            self.totalPage = tpage

        print('内容数量：', len(res))
        pass
        for i in res:
            itim = {}
            # 取属性 过滤掉表头
            class_ = str(i.xpath('./@class').extract())
            if (class_[0] == 'gridHeader'):
                pass
            else:
                # //*[@id="699db746-cf82-4cb4-883d-20e43227c055"]/td[3]/a
                context = i.xpath('./td[3]/a/@href').extract()
                for c in context:
                    url = c.split('&')[2] + "&" + c.split('&')[3]
                    print('---->爬内容 延时 ')
                    time.sleep(0.08)
                    yield scrapy.Request(self.secUrl + url, callback=self.detail_parse, dont_filter=True)

            yield itim  # 有yielad是个生成器  --不会中段 如果是在for循环中下次是从循环开始的地方开始
        # 查下一页数据
        if self.totalPage != None and int(self.currentPage) <= int(self.totalPage):
            print('---->爬分页 延时 ', self.currentPage)

            time.sleep(0.03)
            self.currentPage = self.currentPage + 1
            print('================= 第', self.currentPage, '页')
            yield scrapy.FormRequest(
                url='https://www.landchina.com/default.aspx?tabid=263&ComName=default',
                formdata={
                    'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                    'TAB_QuerySubmitConditionData': '9f2c3acd-0256-4da2-a659-6949c4671a2a:2015-1-1~',  # 开始日期
                    'TAB_QuerySubmitPagerData': str(self.currentPage)  # 开始页码
                },
                callback=self.parse
            )

    def detail_parse(self, response):

        x_ = '//table[@class="theme"]/tbody/tr'
        trs = response.xpath(x_)

        obj = {
            'adminLoc': '',
            'location': '',
            'area': '',
            'use': '',
            'gdfs': '',
            'useYear': '',
            'dealPrice': '',
            'jdTime': '',
            'htime': ''
        }
        # 行政区
        if trs[2].xpath('./td')[1].xpath('./span/text()').extract():
            adminLoc = trs[2].xpath('./td')[1].xpath('./span/text()').extract()[0]
            obj['adminLoc'] = adminLoc
        # 项目位置
        if trs[4].xpath('./td')[1].xpath('./span/text()').extract():
            location = trs[4].xpath('./td')[1].xpath('./span/text()').extract()[0]
            obj['location'] = location

        # 面积(公顷)
        if trs[5].xpath('./td')[1].xpath('./span/text()').extract():
            area = trs[5].xpath('./td')[1].xpath('./span/text()').extract()[0]
            obj['area'] = area
        # 土地用途
        if trs[6].xpath('./td')[1].xpath('./span/text()').extract():
            use = trs[6].xpath('./td')[1].xpath('./span/text()').extract()[0]
            obj['use'] = use
        # 供地方式
        if trs[6].xpath('./td')[3].xpath('./span/text()').extract():
            gdfs = trs[6].xpath('./td')[3].xpath('./span/text()').extract()[0]
            obj['gdfs'] = gdfs
        # 使用年限
        if trs[7].xpath('./td')[1].xpath('./span/text()').extract():
            useYear = trs[7].xpath('./td')[1].xpath('./span/text()').extract()[0]
            obj['useYear'] = useYear
        # dealPrice
        if trs[8].xpath('./td')[3].xpath('./span/text()').extract():
            dealPrice = trs[8].xpath('./td')[3].xpath('./span/text()').extract()[0]
            obj['dealPrice'] = dealPrice
        # 约定交地时间
        if trs[12].xpath('./td')[3].xpath('./span/text()').extract():
            jdTime = trs[12].xpath('./td')[3].xpath('./span/text()').extract()[0]
            obj['jdTime'] = jdTime
        # 合同签订时间
        if trs[15].xpath('./td')[3].xpath('./span/text()').extract():
            htime = trs[15].xpath('./td')[3].xpath('./span/text()').extract()[0]
            obj['htime'] = htime
        self.totalData = self.totalData + 1

        # 写mysql
        sql = 'insert into landchina(admin_loc,location,area,`use`,gdfs,use_year,deal_price,jd_time,ht_time) values ' \
              '("%s","%s","%s","%s","%s","%s","%s","%s","%s") '

        sql = sql % (
            str(obj['adminLoc']), str(obj['location']), str(obj['area']), str(obj['use']), str(obj['gdfs']),
            str(obj['useYear']), str(obj['dealPrice']),
            str(obj['jdTime']), str(obj['htime']))

        print(':::::', sql)

        cur.execute(sql)
        con.commit()

        print(self.totalData)
        pass

