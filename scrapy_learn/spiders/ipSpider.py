# -*- coding: utf-8 -*-
import scrapy


class ProxytestSpider(scrapy.Spider):
    name = 'ipSpider'
    # allowed_domains = ['douban.com']
    i = 1
    start_urls = ['https://proxy.mimvp.com/freesecret.php?proxy=in_hp&sort=&page=1']

    def parse(self, response):
        # //td[@class="tbl-proxy-port"]
        url_xpath = '//td[@class="tbl-proxy-ip"] | //td[@class="tbl-proxy-port"]'
        # url_xpath = '//td[@class="tbl-proxy-ip"]/parent::*'

        res = response.xpath(url_xpath)
        # 先解析结果判断是不是最后一页
        itim = {"ip": None, "port": None}
        for con in res:

            if (con.extract()).__contains__('ip'):
                ip = con.xpath("text()").extract()
                itim['ip'] = ip

                pass
            if (con.extract()).__contains__('port'):
                port = con.xpath("./img/@src").extract()
                itim['port'] = port

                pass
            if itim['ip'] and itim['port']:
                yield itim
                itim = {"ip": None, "port": None}
                pass
            # 构造下一个url
            self.i += 1
            next_url = 'https://proxy.mimvp.com/freesecret.php?proxy=in_hp&sort=&page=%s' % self.i
            print("页码：",self.i)

            yield scrapy.Request(next_url, callback=self.parse)
