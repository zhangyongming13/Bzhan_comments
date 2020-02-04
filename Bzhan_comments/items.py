# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BzhanCommentsItem(scrapy.Item):
    comment_author_mid = scrapy.Field()
    comment_author_avatar = scrapy.Field()
    comment_author_name = scrapy.Field()
    comment_date = scrapy.Field()
    comment_text = scrapy.Field()
    # 评论的mid，mid和media_id确定一个评论的唯一
    comment_mid = scrapy.Field()
    # 被评论的番剧的id号
    media_id = scrapy.Field()
    score = scrapy.Field()
    comment_likes = scrapy.Field()
    comment_disliked = scrapy.Field()
    comment_liked = scrapy.Field()
    last_index_show = scrapy.Field()
