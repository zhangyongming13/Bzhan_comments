# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class BzhanCommentsPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        sheet_name = settings['MONGODB_SHEETNAME']

        # 初始化mongodb连接并返回
        mongo_client = pymongo.MongoClient(host=host, port=port)
        mongo_db = mongo_client[db_name]
        self.mongo_object = mongo_db[sheet_name]

    def process_item(self, item, spider):
        try:
            # 每一个评论数据插入mongodb数据库
            mongodb_data_dict = dict(item)
            self.mongo_object.insert(mongodb_data_dict)
            print('%s 的评论保存到mongodb数据库成功！' % item['comment_author'])
        except Exception as e:
            print('保存到mongodb数据库失败，原因：' + str(e))
        return item
