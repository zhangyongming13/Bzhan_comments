# -*- coding: utf-8 -*-

# Scrapy settings for Bzhan_comments project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os

BOT_NAME = 'Bzhan_comments'

SPIDER_MODULES = ['Bzhan_comments.spiders']
NEWSPIDER_MODULE = 'Bzhan_comments.spiders'

SPIDER_TEXT = 'folkCommentUrl.txt'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Bzhan_comments (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 3
DEFAULT_REQUEST_HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'

ITEM_PIPELINES = {
   'Bzhan_comments.pipelines.BzhanCommentsPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'Bzhan_comments.middlewares.RandomUserAgent': 3,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# 使用mongodb数据库的设置
MONGODB_HOST = str(os.getenv('MONGODB_HOST'))
MONGODB_DBNAME = str(os.getenv('MONGODB_DBNAME'))
MONGODB_PORT = int(os.getenv('MONGODB_PORT'))
MONGODB_PASSWD = str(os.getenv('MONGODB_PASSWD'))
MONGODB_AUTHDB= str(os.getenv('MONGODB_AUTHDB'))
MONGODB_USER = str(os.getenv('MONGODB_USER'))
MONGODB_SHEETNAME_1 = str(os.getenv('MONGODB_SHEETNAME_1'))

# 使用mysql数据库的设置
MYSQL_HOST = str(os.getenv('MYSQL_HOST'))
MYSQL_USER = str(os.getenv('MYSQL_USER'))
MYSQL_PASSWD = str(os.getenv('MYSQL_PASSWD'))
MYSQL_DB = str(os.getenv('MYSQL_DB'))

START_URL = str(os.getenv('START_URL'))

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Bzhan_comments.middlewares.BzhanCommentsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Bzhan_comments.middlewares.BzhanCommentsDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'Bzhan_comments.pipelines.BzhanCommentsPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
