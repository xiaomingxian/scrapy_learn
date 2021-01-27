import scrapy


class fundSpider(scrapy.Spider):
    name = 'fundSpider'
    start_urls = ['http://vip.stock.finance.sina.com.cn/fund_center/index.html#hbphall']

    def parse(self, response):
        print('---------__>>>>>>>>>')

        xpath = '//*[@id="cHBPH"]/table/tbody/tr[1]/td[2]'

        res = response.xpath(xpath)
        print(res)
        pass
