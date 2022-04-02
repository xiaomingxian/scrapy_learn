# -*- coding: utf-8 -*-
import scrapy




class IptestSpider(scrapy.Spider):
    name = 'landf'
    allowed_domains = ['landchina.mnr.gov.cn']
    # start_urls = ['http://landchina.mnr.gov.cn/land/jggg/gpcr1/202006/t20200610_7476600.htm']  # 开始爬取的位置
    urls = []  # 开始爬取的位置
    index = 0
    file_name = None

    def __init__(self, f=None, *args, **kwargs):
        super(IptestSpider, self).__init__(*args, **kwargs)
        self.file_name = f

    def start_requests(self):

        # file = open("C:\\Users/仙/Desktop/links_pure.txt")
        file = open(
            "/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/file30/" + str(
                self.file_name) + '.txt')

        while True:
            text = file.readline()  # 只读取一行内容
            # 判断是否读取到内容
            if not text:
                break
            # self.start_urls.append(text)
            url = text.replace('\n', '')
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

        print('------->>>>>    结束   SUCCESS     ')

    # start_urls结果返回到parse
    def parse(self, response):
        url = response.request.url

        # 行政区
        obj = {
            'xzq': '',
            'xmmc': '',
            'xmwz': '',
            'gymj': '',
            'clmj': '',
            'gdfs': '',
            'tdyt': '',
            'synx': '',
            'hyfl': '',
            'tdjb': '',
            'cjjg': '',
            'zfqh': '',
            'ydzfrq': '',
            'ydzfje': '',
            'tdsyqr': '',
            'bz': '',
            'ydrjlx': '',
            'ydrjls': '',
            'ydjdsj': '',
            'ydkgsj': '',
            'ydjgsj': '',
            'sjkgsj': '',
            'sjjgsj': '',
            'pzdw': '',
            'htqdrq': '',
            'url': url

        }
        obj['url'] = url
        xpath_url = '//div[@class="gu-art-con"]/table/tr[2]/td[2]/text()'
        if len(response.xpath(xpath_url).extract()):
            xzq = response.xpath(xpath_url).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['xzq'] = xzq

        xmmc_u = '//div[@class="gu-art-con"]/table/tr[3]/td[2]/text()'
        if len(response.xpath(xmmc_u).extract()):
            xmmc = response.xpath(xmmc_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['xmmc'] = xmmc

        xmwz_u = '//div[@class="gu-art-con"]/table/tr[4]/td[2]/text()'
        if len(response.xpath(xmwz_u).extract()):
            xmwz = response.xpath(xmwz_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['xmwz'] = xmwz

        gymj_u = '//div[@class="gu-art-con"]/table/tr[5]/td[2]/text()'
        if len(response.xpath(gymj_u).extract()):
            gymj = response.xpath(gymj_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['gymj'] = gymj

        clmj_u = '//div[@class="gu-art-con"]/table/tr[5]/td[4]/text()'
        if len(response.xpath(clmj_u).extract()):
            clmj = response.xpath(clmj_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['clmj'] = clmj

        tdyt_u = '//div[@class="gu-art-con"]/table/tr[6]/td[2]/text()'
        if response.xpath(tdyt_u).extract():
            tdyt = response.xpath(tdyt_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['tdyt'] = tdyt

        gdfs_u = '//div[@class="gu-art-con"]/table/tr[6]/td[4]/text()'
        if len(response.xpath(gdfs_u).extract()):
            gdfs = response.xpath(gdfs_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['gdfs'] = gdfs

        synx_u = '//div[@class="gu-art-con"]/table/tr[7]/td[2]/text()'
        if len(response.xpath(synx_u).extract()):
            synx = response.xpath(synx_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['synx'] = synx

        hyfl_u = '//div[@class="gu-art-con"]/table/tr[7]/td[4]/text()'
        if len(response.xpath(hyfl_u).extract()):
            hyfl = response.xpath(hyfl_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['hyfl'] = hyfl

        tdjb_u = '//div[@class="gu-art-con"]/table/tr[8]/td[2]/text()'
        if len(response.xpath(tdjb_u).extract()):
            tdjb = response.xpath(tdjb_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['tdjb'] = tdjb

        cjjg_u = '//div[@class="gu-art-con"]/table/tr[8]/td[4]/text()'
        if len(response.xpath(cjjg_u).extract()):
            cjjg = response.xpath(cjjg_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['cjjg'] = cjjg

        # /table/tbody/tr[2]/td[1]/text()

        zfqh_u = '//div[@class="gu-art-con"]/table/tr[9]/td[2]/table/tr[2]/td[1]/text()'
        if len(response.xpath(zfqh_u).extract()):
            zfqh = response.xpath(zfqh_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['zfqh'] = zfqh

        ydzfrq_u = '//div[@class="gu-art-con"]/table/tr[9]/td[2]/table/tr[2]/td[2]/script'
        if len(response.xpath(ydzfrq_u).extract()):
            ydzfrq = \
                response.xpath(ydzfrq_u).extract()[0].replace('\n', '').replace('  ', '').split('var a = \'')[1].split(
                    '\';')[0]
            obj['ydzfrq'] = ydzfrq

        ydzfje_u = '//div[@class="gu-art-con"]/table/tr[9]/td[2]/table/tr[2]/td[3]/text()'
        if len(response.xpath(ydzfje_u).extract()):
            ydzfje = response.xpath(ydzfje_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['ydzfje'] = ydzfje

        bz_u = '//div[@class="gu-art-con"]/table/tr[9]/td[2]/table/tr[2]/td[4]/text()'
        if (len(response.xpath(bz_u).extract())):
            bz = response.xpath(bz_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['bz'] = bz

        tdsyqr_u = '//div[@class="gu-art-con"]/table/tr[10]/td[2]/text()'
        if len(response.xpath(tdsyqr_u).extract()):
            tdsyqr = response.xpath(tdsyqr_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['tdsyqr'] = tdsyqr

        ydrjlx_u = '//div[@class="gu-art-con"]/table/tr[11]/td[2]/table/tr[1]/td[2]/text()'
        if len(response.xpath(ydrjlx_u).extract()):
            ydrjlx = response.xpath(ydrjlx_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['ydrjlx'] = ydrjlx

        ydrjls_u = '//div[@class="gu-art-con"]/table/tr[11]/td[2]/table/tr[1]/td[4]/text()'
        if len(response.xpath(ydrjls_u).extract()):
            ydrjls = response.xpath(ydrjls_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['ydrjls'] = ydrjls

        ydjdsj_u = '//div[@class="gu-art-con"]/table/tr[11]/td[4]/text()'
        if (len(response.xpath(ydjdsj_u).extract())):
            ydjdsj = response.xpath(ydjdsj_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['ydjdsj'] = ydjdsj

        ydkgsj_u = '//div[@class="gu-art-con"]/table/tr[12]/td[2]/text()'
        if (len(response.xpath(ydkgsj_u).extract())):
            ydkgsj = response.xpath(ydkgsj_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['ydkgsj'] = ydkgsj

        ydjgsj_u = '//div[@class="gu-art-con"]/table/tr[12]/td[4]/text()'
        if (len(response.xpath(ydjgsj_u).extract())):
            ydjgsj = response.xpath(ydjgsj_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['ydjgsj'] = ydjgsj

        sjkgsj_u = '//div[@class="gu-art-con"]/table/tr[13]/td[2]/text()'
        if (len(response.xpath(sjkgsj_u).extract())):
            sjkgsj = response.xpath(sjkgsj_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['sjkgsj'] = sjkgsj

        sjjgsj_u = '//div[@class="gu-art-con"]/table/tr[13]/td[4]/text()'
        if (len(response.xpath(sjjgsj_u).extract())):
            sjjgsj = response.xpath(sjjgsj_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['sjjgsj'] = sjjgsj

        pzdw_u = '//div[@class="gu-art-con"]/table/tr[14]/td[2]/text()'
        if (len(response.xpath(pzdw_u).extract())):
            pzdw = response.xpath(pzdw_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['pzdw'] = pzdw

        htqdrq_u = '//div[@class="gu-art-con"]/table/tr[14]/td[4]/text()'
        if (len(response.xpath(htqdrq_u).extract())):
            htqdrq = response.xpath(htqdrq_u).extract()[0].replace(' ', '').replace('\xa0\xa0\n', '')
            obj['htqdrq'] = htqdrq

        try:

            fr = open("/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/res/"+str(self.file_name), 'a')
            fr.write(str(obj) + '\n')
            fr.close()


            print(
                '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SSSSSSSSSSSSSSSSS 写入文件成功 SSSSSSSSSSSSSSSSS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        except Exception as e:
            print('::::异常信息：：', e)
            print('==========@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   写入文件失败=========', url)
            f = open("/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/fail_url2", 'a')
            f.write(url + '\n')
            f.close()
        # print('=======>>对象:', obj)
        print('---------------------->>>>>>>>>>>>>>>>>>>>>>>>>', self.index)
        self.index = self.index + 1
