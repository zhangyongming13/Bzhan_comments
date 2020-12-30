import scrapy
import json
import time
import random
import pymysql
import os
from Bzhan_comments.items import BzhanCommentsItem
from mongoTomysql import mongoTomysql
from Bzhan_comments import settings


def get_url_delete_url(file_path):
    """
    从文件中读取爬取的url，然后删除掉url的行，
    :param file_path:
    :return: 读取的url
    """
    with open(file_path, 'r', encoding='utf8') as f:
        data = f.readlines()
        if data:
            url = data[0].split(' ')[-1].strip('\n')
            data = data[1:]
            with open(file_path, 'w', encoding='utf8') as wf:
                wf.writelines(data)
        else:
            return None
    return url


class bzhan_comment(scrapy.Spider):
    mongoTomysql = mongoTomysql()
    name = "bzhan_comment"
    allowed_domains = ["bilibili.com"]
    urlPrefix = 'https://api.bilibili.com/pgc/review/short/list?media_id='
    start_urls = []
    if os.path.isfile(settings.START_URL):
        with open(settings.START_URL, 'r', encoding='utf8') as f:
            allUrl = f.read().split('\n')[0:-1]
            # 判断最后一个url（即将要进行爬取的startUrl）是否在前面已经出现过，出现过就是重复的了
            if allUrl[-1] in allUrl[0:-2]:
                # 判断folkCommentUrl.txt文件中是否有待爬取的
                url_from_text = get_url_delete_url(settings.SPIDER_TEXT)
                if url_from_text:
                    start_urls.append(url_from_text)
                else:
                    print('重复爬取并且folkCommentUrl.txt文件中没有待爬取的url！')
            else:
                start_urls.append(allUrl[-1])
    # start_url文件不存在，直接从folkCommentUrl.txt文件中判断是否有待爬取番剧
    else:
        url_from_text = get_url_delete_url(settings.SPIDER_TEXT)
        if url_from_text:
            start_urls.append(url_from_text)
        else:
            print("folkCommentUrl.txt文件中没有待爬取的url！")

    # 初始化mysql连接并返回
    mysqlHost = settings.MYSQL_HOST
    mysqlUser = settings.MYSQL_USER
    mysqlPasswd = settings.MYSQL_PASSWD
    mysqlDb = settings.MYSQL_DB
    connection = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPasswd, db=mysqlDb)
    mysql_cursor = connection.cursor()

    def judge_exist(self, comment_mid, media_id):
        """
        判断评论是否已在数据库中，通过comment_mid和media_id两个主键确认
        :param comment_mid: 评论的id即评论的创建用户
        :param media_id: 被评论番剧的番剧id
        :return: 评论是否已经在数据库中的结果
        """
        # 参数化查询可以避免sql注入问题
        sql = r'select comment_author_mid from bzhan_comment where media_id = %s and comment_mid = %s'
        self.mysql_cursor.execute(sql, (media_id, comment_mid))
        result = self.mysql_cursor.fetchall()
        return result

    def parse(self, response):
        # 记录爬取是否重复了，重复的话结束爬取
        flag = 0
        longTimesleep = 0
        media_id = ''
        item = BzhanCommentsItem()
        comment_data = response.text

        # 将json数据转换为python数据
        comment_data = json.loads(comment_data, encoding='utf8')
        cursor = str(comment_data['data']['next'])
        comment_data = comment_data['data']['list']
        for i in range(len(comment_data)):
            # 获取具体数据
            try:
                item['comment_author_mid'] = comment_data[i]['author']['mid']
                item['comment_author_avatar'] = comment_data[i]['author']['avatar']
                item['comment_author_name'] = comment_data[i]['author']['uname']
                item['comment_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment_data[i]['ctime']))
                item['comment_text'] = comment_data[i]['content']
                item['comment_mid'] = comment_data[i]['mid']
                item['media_id'] = comment_data[i]['media_id']
                media_id = str(comment_data[i]['media_id'])
                item['score'] = comment_data[i]['score']
                try:
                    item['comment_likes'] = comment_data[i]['stat']['likes']
                except Exception as e:
                    item['comment_likes'] = 0
                try:
                    item['comment_disliked'] = comment_data[i]['stat']['disliked']
                except Exception as e:
                    item['comment_disliked'] = 0
                try:
                    item['comment_liked'] = comment_data[i]['stat']['liked']
                except Exception as e:
                    item['comment_liked'] = 0
                try:
                    item['last_index_show'] = comment_data[i]['progress']
                except Exception as e:
                    item['last_index_show'] = ""
                # 判断该评论是否已经存在
                if not self.judge_exist(item['comment_mid'], item['media_id']):
                    yield item
            except Exception as e:
                print(e)
                longTimesleep += 1
                print('缺少关键数据，该评论数据放弃')
        try:
            time.sleep(random.randint(4, 10) + random.randint(0, 9) / 10)
            if longTimesleep != 0:
                url = response.url
                print('检查到返回的数据出错！延长休眠时间！')
                time.sleep(random.randint(36, 48) + random.randint(0, 9) / 10)
            else:
                if cursor != '0':
                    url = self.urlPrefix + media_id + '&ps=20&sort=0&cursor=' + cursor
                    if os.path.isfile(settings.START_URL):
                        # 判断该url是否已经爬取过了
                        with open(settings.START_URL, 'r', encoding='utf8') as f:
                            allUrl = f.read().split('\n')[0:-1]
                            # 该url已经爬取过了
                            if url in allUrl:
                                # 判断folkCommentUrl.txt文件中是否有待爬取的
                                url_from_text = get_url_delete_url(settings.SPIDER_TEXT)
                                if url_from_text:
                                    url = url_from_text
                                else:
                                    flag += 1
                # 这个番剧已经爬取完毕，需要查看folkCommentUrl.txt中是否含有下一个待爬取的番剧
                else:
                    # 判断folkCommentUrl.txt文件中是否有待爬取的
                    url_from_text = get_url_delete_url(settings.SPIDER_TEXT)
                    if url_from_text:
                        url = url_from_text
                    else:
                        flag += 1
            if flag == 0:
                print('爬取：' + url)
                # 记录下一次要爬取的url，保证意外中断之后从中断的位置开始爬取
                with open(settings.START_URL, 'a', encoding='utf8') as f:
                    f.write(url + '\n')
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)
            else:
                print('重复爬取并且folkCommentUrl.txt文件中没有待爬取的url！')
                self.mongoTomysql.saveDatatomysql()
        except Exception as e:
            print(e)
            print('爬取完毕！')
