import scrapy
import json
import time
import random
from Bzhan_comments.items import BzhanCommentsItem


class bzhan_comment(scrapy.Spider):
    name = "bzhan_comment"
    allowed_domains = ["bilibili.com"]
    start_urls = ['https://bangumi.bilibili.com/review/web_api/short/list?media_id=22718131&folded=0&page_size=20&sort=0']

    def parse(self, response):
        item = BzhanCommentsItem()
        comment_data = response.text

        # 将json数据转换为python数据
        comment_data = json.loads(comment_data, encoding='utf8')
        comment_data = comment_data['result']['list']
        for i in range(len(comment_data)):
            # 获取具体数据
            try:
                item['comment_author'] = comment_data[i]['author']['uname']
                item['comment_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment_data[i]['ctime']))
                item['comment_text'] = comment_data[i]['content']
                item['score'] = comment_data[i]['user_rating']['score']
                try:
                    item['comment_likes'] = comment_data[i]['likes']
                except Exception as e:
                    item['comment_likes'] = 0
                try:
                    item['comment_disliked'] = comment_data[i]['disliked']
                except Exception as e:
                    item['comment_disliked'] = 0
                try:
                    item['comment_liked'] = comment_data[i]['liked']
                except Exception as e:
                    item['comment_liked'] = 0
                try:
                    item['last_index_show'] = comment_data[i]['user_season']['last_index_show']
                except Exception as e:
                    item['last_index_show'] = ""
                yield item
            except Exception as e:
                print('缺少关键数据，该评论数据放弃')
        try:
            cursor = comment_data[-1]['cursor']
            time.sleep(random.randint(4, 14) + random.randint(7, 17) / 10)
            url = str(self.start_urls[0]) + '&cursor=' + cursor
            print('爬取：' + url)
            yield scrapy.Request(url, callback=self.parse)
        except Exception as e:
            print(e)
            print('爬取完毕！')
