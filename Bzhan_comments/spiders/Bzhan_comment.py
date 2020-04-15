import scrapy
import json
import time
import random
from Bzhan_comments.items import BzhanCommentsItem
from mongoTomysql import mongoTomysql


class bzhan_comment(scrapy.Spider):
    mongoTomysql = mongoTomysql()
    name = "bzhan_comment"
    allowed_domains = ["bilibili.com"]
    urlPrefix = 'https://api.bilibili.com/pgc/review/short/list?media_id='
    start_urls = []
    with open('startUrl.txt', 'r', encoding='utf8') as f:
        allUrl = f.read().split('\n')[0:-1]
        # 判断最后一个url（即将要进行爬取的startUrl）是否在前面已经出现过，出现过就是重复的了
        if allUrl[-1] in allUrl[0:-2]:
            print('重复爬取，结束！')
        else:
            start_urls.append(allUrl[-1])

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
                url = self.urlPrefix + media_id + '&ps=20&sort=0&cursor=' + cursor
                # 判断该url是否已经爬取过了
                with open('startUrl.txt', 'r', encoding='utf8') as f:
                    allUrl = f.read().split('\n')[0:-1]
                    if url in allUrl:
                        flag += 1
                # 记录下一次要爬取的url，保证意外中断之后从中断的位置开始爬取
                with open('startUrl.txt', 'a', encoding='utf8') as f:
                    f.write(url + '\n')
            if flag == 0:
                print('爬取：' + url)
                yield scrapy.Request(url, callback=self.parse)
            else:
                print('重复爬取，爬取结束！')
                self.mongoTomysql.saveDatatomysql()
        except Exception as e:
            print(e)
            print('爬取完毕！')
