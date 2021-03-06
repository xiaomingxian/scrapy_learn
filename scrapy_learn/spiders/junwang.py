# -*- coding: utf-8 -*-
import scrapy


class BaiduSpiderSpider(scrapy.Spider):
    name = 'jw'
    allowed_domains = ['huaban.com']
    start_urls = ['https://www.landchina.com/default.aspx?tabid=263&ComName=default']  # 开始爬取的位置
    qianzuhi = 'landchina.com'

    # start_urls结果返回到parse
    def parse(self, response):
        # xpath解析
        print('======>', response)
        # 结果
        list = []

        xpath_url = '//@href'
        # xpath_url = '//@div'
        res = response.xpath(xpath_url)
        # print('内容数量：', len(res))
        for i in res:
            itim = {}
            # flag=0
            # # print(str(i.extract()))
            # if str(i.extract()).endswith('css'):
            #     itim['css'] = i.extract()
            #     flag=1
            # if str(i.extract()).endswith('png'):
            #     itim['pic'] = i.extract()
            #     flag=1
            # if flag:
            #     list.append(itim)
            #     yield itim
            itim['msg'] = i.extract
            yield itim#有yielad是个生成器  --不会中段 如果是在for循环中下次是从循环开始的地方开始
        # Spider must return Request, BaseItem, dict or None, got 'list' in <GET https://huaban.com/>
        # yield list
