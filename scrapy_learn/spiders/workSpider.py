# -*- coding: utf-8 -*-
import scrapy


class ProxytestSpider(scrapy.Spider):
    name = 'work'
    allowed_domains = ['allowed_domains']
    # start_urls = ['https://proxy.mimvp.com/freesecret.php?proxy=in_hp&sort=&page=1']
    start_urls = ['http://whois.chinaz.com/client.cn']

    # def start_requests(self):
    #     self.name = 'work'
    #     self.start_urls = ['http://whois.chinaz.com/client.cn']
    #     pass

    def parse(self, response):
        x_ = '//ul[@id="sh_info"]//li'
        res = response.xpath(x_)
        for i in res:
            # 获取li下的div
            left = i.xpath('./div[@class="fl WhLeList-left"]')
            right = i.xpath('./div[@class="fr WhLeList-right"]')
            status = i.xpath('./div[@class="fr WhLeList-right clearfix"]')
            other = i.xpath('./div[@class="fr WhLeList-right block ball lh24"]')
            yuName = i.xpath('./div[@class="fl WhLeList-left h64"]')

            # 注册商，创建时间，过期时间，DNS
            if left and right:
                l = left.xpath('./text()').extract()
                r = ''
                if l[0] == 'DNS':
                    r = right.xpath('./text()').extract()
                elif '时间' in l[0]:
                    r = right.xpath('./span/text()').extract()
                else:
                    r = right.xpath('./div/span/text()').extract()

                print(l, '-----', r)
            # 状态
            if left and status:
                l = left.xpath('./text()').extract()
                r = status.xpath('./p/span/text()').extract()

                print(l, '-----', r)
            # 域名
            if yuName and right:
                l = yuName.xpath('./span/text()').extract()
                ys = right.xpath('./p/a')
                y_list = []
                for y in ys:
                    y_list.append(y.xpath('./text()').extract())

                print(l, '-----', y_list)
            #    联系人，邮箱
            if left and other:
                l = left.xpath('./text()').extract()
                r = other.xpath('./span/text()').extract()
                print(l, '-----', r)
