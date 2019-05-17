# -*- coding: utf-8 -*-
import scrapy
import re


class CnWorkSpider(scrapy.Spider):
    name = 'cn_work'
    # allowed_domains = ['http://whois.chinaz.com/suffix']
    total=0
    currentPage=1;
    url='http://whois.chinaz.com/suffix?sx=&suffix=&z_suffix=&c_suffix=&time=30&startDay=&endDay=&st=&cn=&city=&page='
    start_urls = ['http://whois.chinaz.com/suffix?sx=&suffix=&z_suffix=&c_suffix=&time=30&startDay=&endDay=&st=&cn=&city=&page=1']

    def parse(self, response):

        # 先解析分页信息
        # page_x='//*[@id="pagelist"]/span[1]/text()'
        # p_res=response.xpath(page_x).extract()
        # print('====总页数：',p_res[0])
        # s=int(re.sub('\D','',p_res[0]))
        # self.total=s
        # 解析到第6叶需要登陆
        self.total=6




        x_path='//*[@id="ajaxInfo"]/ul/li/div/div/a/@href'
        res=response.xpath(x_path)
        itim={}
        for i in res:
            if '/reverse?host=' in i.extract():
                pass
            else:
                itim['cn']=i.extract()
                yield itim
        # 构造下一个请求
        if self.currentPage<self.total:
            next_url=self.url+str(self.currentPage)
            yield scrapy.Request(next_url,callback=self.parse)
            self.currentPage+=1

        pass
