# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_learn project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_learn'
# 日志级别由高到低
LOG_LEVEL = 'ERROR'
# LOG_LEVEL = 'WARNING'
# LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'DEBUG'
# LOG_FILE='./log.log'


SPIDER_MODULES = ['scrapy_learn.spiders']
NEWSPIDER_MODULE = 'scrapy_learn.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# 模拟浏览器请求
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapy_learn.middlewares.ScrapyLearnSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# 将代理类添加到中间件列表中
DOWNLOADER_MIDDLEWARES = {
    'scrapy_learn.middlewares.ScrapyLearnDownloaderMiddleware': 543,
    # 'scrapy_learn.middlewares.ProxyMiddleware': 544,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 有多个item管道 每个item都会经过
ITEM_PIPELINES = {
    #  要开启的pipline的位置 300距离引擎的远近，距离引擎越近越早执行    范围 0-1000
    'scrapy_learn.pipelines.ScrapyLearnPipeline': 300,
    # 'scrapy_learn.pipelines.TestPipeline': 200,
    'scrapy_learn.pipelines.ipPipleLine': 200,
    'scrapy_learn.pipelines.workPipleLine': 100,
}
# 开启piplines

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 代理ip
PROXIES = ['http://183.207.95.27:80', 'http://111.6.100.99:80', 'http://122.72.99.103:80',
           'http://106.46.132.2:80', 'http://112.16.4.99:81', 'http://123.58.166.113:9000',
           'http://118.178.124.33:3128', 'http://116.62.11.138:3128', 'http://121.42.176.133:3128',
           'http://111.13.2.131:80', 'http://111.13.7.117:80', 'http://121.248.112.20:3128',
           'http://112.5.56.108:3128', 'http://42.51.26.79:3128', 'http://183.232.65.201:3128',
           'http://118.190.14.150:3128', 'http://123.57.221.41:3128', 'http://183.232.65.203:3128',
           'http://166.111.77.32:3128', 'http://42.202.130.246:3128', 'http://122.228.25.97:8101',
           'http://61.136.163.245:3128', 'http://121.40.23.227:3128', 'http://123.96.6.216:808',
           'http://59.61.72.202:8080', 'http://114.141.166.242:80', 'http://61.136.163.246:3128',
           'http://60.31.239.166:3128', 'http://114.55.31.115:3128', 'http://202.85.213.220:3128']
