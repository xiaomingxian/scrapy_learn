from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    # for i in range(0,10):
    #     print(i)
    settings = get_project_settings()

    crawler = CrawlerProcess(settings)
    # for i in range(0,1):
    for i in range(0,31):
        print(i)
        crawler.crawl('landd',f=i)  # 爬虫名

    crawler.start()
