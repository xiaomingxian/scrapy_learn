import scrapy


class fundSpider(scrapy.Spider):
    name = 'leetCode'
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html']

    def parse(self, response):

        xpath = '//tr[@class="provincetr"]/td/a'

        res = response.xpath(xpath)

        for i in res:
            text = i.xpath('./text()')[0]
            url = i.xpath('./@href')[0]
            next_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/' + url.extract()
            yield scrapy.Request(next_url, callback=self.city_parse)
            print(text.extract(), next_url)

    def city_parse(self, response):
        xpath_city = '//tr[@class="citytr"]'
        res_city = response.xpath(xpath_city)

        for c in res_city:
            city_code = c.xpath('./td[1]/a/text()').extract()[0]
            city_name = c.xpath('./td[2]/a/text()').extract()[0]
            city_url = c.xpath('./td[2]/a/@href').extract()[0]
            print('city code:', city_code, city_name, city_url)
            next_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/' + city_url
            yield scrapy.Request(next_url, callback=self.country_parse)

    def country_parse(self, response):
        xpath_country = '//tr[@class="countytr"]'
        res_country = response.xpath(xpath_country)
        for c in res_country:
            country_code = None
            country_name = None
            country_url = None
            if len(c.xpath('./td[1]/a/text()').extract()) == 0:
                country_code = c.xpath('./td[1]/text()').extract()[0]
                country_name = c.xpath('./td[2]/text()').extract()[0]
            else:
                country_code = c.xpath('./td[1]/a/text()').extract()[0]
                country_name = c.xpath('./td[2]/a/text()').extract()[0]
                country_url = c.xpath('./td[2]/a/@href').extract()[0]
                split_arry = response.url.split('/')
                need_replace = split_arry[len(split_arry) - 1]
                next_url = response.url.replace(need_replace, country_url)
                yield scrapy.Request(next_url, callback=self.town_parse)

            print('country:::', country_code, country_name, country_url)
            pass
        pass

    def town_parse(self, response):
        xpath_town = '//tr[@class="towntr"]'
        res_town = response.xpath(xpath_town)
        for c in res_town:
            town_code = None
            town_name = None
            town_url = None
            if len(c.xpath('./td[1]/a/text()').extract()) == 0:
                town_code = c.xpath('./td[1]/text()').extract()[0]
                town_name = c.xpath('./td[2]/text()').extract()[0]
            else:
                town_code = c.xpath('./td[1]/a/text()').extract()[0]
                town_name = c.xpath('./td[2]/a/text()').extract()[0]
                town_url = c.xpath('./td[2]/a/@href').extract()[0]
        print('tttttttttttsss::::', town_code, town_name, town_url)


if __name__ == '__main__':
    xx = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/65/6543.html'
    s = xx.split('/')[len(xx.split('/')) - 1]
    print(s)
    xs = xx.replace(s, 'asasas')
    print(xs)
    pass
