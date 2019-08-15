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
    comment_likes = scrapy.Field()
    comment_disliked = scrapy.Field()
    comment_liked = scrapy.Field()
    last_index_show = scrapy.Field()
