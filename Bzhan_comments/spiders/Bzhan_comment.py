import scrapy
import json
import time
import random
from Bzhan_comments.items import BzhanCommentsItem


class bzhan_comment(scrapy.Spider):
    name = "bzhan_comment"
    allowed_domains = ["bilibili.com"]
    urlPrefix = 'https://api.bilibili.com/pgc/review/short/list?media_id=22718131&ps=20&sort=0'
    start_urls = []
    with open('startUrl.txt', 'r', encoding='utf8') as f:
        start_urls.append(f.read().split('\n')[-2])

    def parse(self, response):
        item = BzhanCommentsItem()
        comment_data = response.text

        # 将json数据转换为python数据
        comment_data = json.loads(comment_data, encoding='utf8')
        cursor = str(comment_data['data']['next'])
        comment_data = comment_data['data']['list']
        for i in range(len(comment_data)):
            # 获取具体数据
            try:
                item['comment_author'] = comment_data[i]['author']['uname']
                item['comment_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment_data[i]['ctime']))
                item['comment_text'] = comment_data[i]['content']
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
                print('缺少关键数据，该评论数据放弃')
        try:
            time.sleep(random.randint(4, 14) + random.randint(7, 17) / 10)
            url = self.urlPrefix + '&cursor=' + cursor
            # 记录下一次要爬取的url，保证意外中断之后从中断的位置开始爬取
            with open('startUrl.txt', 'a', encoding='utf8') as f:
                f.write(url + '\n')
            print('爬取：' + url)
            yield scrapy.Request(url, callback=self.parse)
        except Exception as e:
            print(e)
            print('爬取完毕！')
