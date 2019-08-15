from scrapy import cmdline


cmdline.execute("scrapy crawl bzhan_comment -s LOG_FILE=all.log".split())
