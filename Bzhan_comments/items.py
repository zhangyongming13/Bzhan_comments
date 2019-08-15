# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BzhanCommentsItem(scrapy.Item):
    comment_author = scrapy.Field()
    comment_date = scrapy.Field()
    comment_text = scrapy.Field()
    score = scrapy.Field()
    comment_like = scrapy.Field()
