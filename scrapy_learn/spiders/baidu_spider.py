# -*- coding: utf-8 -*-
import scrapy


class BaiduSpiderSpider(scrapy.Spider):
    name = 'huaban'
    allowed_domains = ['huaban.com']
    start_urls = ['https://huaban.com/']  # 开始爬取的位置
    qianzuhi = 'huaban.com'
    file_root = 'C:\\xxm\\learn\\python_workspace\\scrapy_result'

    # start_urls结果返回到parse
    def parse(self, response):
        # xpath解析
        # print('======>', response)
        # 结果
        list=[]

        xpath_url = '//@href'
        res = response.xpath(xpath_url)
        # print('内容数量：', len(res))
        for i in res:
            itim = {}
            flag=0
            # print(str(i.extract()))
            if str(i.extract()).endswith('css'):
                itim['css'] = i.extract()
                flag=1
            if str(i.extract()).endswith('png'):
                itim['pic'] = i.extract()
                flag=1
            if flag:
                list.append(itim)
                yield itim
        # Spider must return Request, BaseItem, dict or None, got 'list' in <GET https://huaban.com/>
        # yield list