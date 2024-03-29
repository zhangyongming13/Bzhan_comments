import requests
import time
import random
import pymysql
from tool.GetDataFromEnv import get_data_from_env
from fake_useragent import UserAgent


# 获取B站所有的番剧信息，然后存储到Mysql数据库
class GetFanJuData(object):
    def __init__(self):
        self.basePreUrl = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1' \
                          '&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page='
        self.baseSuffixUrl = '&season_type=1&pagesize=20&type=1'
        self.page = 1
        self.pageUrl = self.basePreUrl + str(self.page) + self.baseSuffixUrl
        self.result = []

        # 初始化mysql链接
        data_dict = get_data_from_env()
        self.connections = pymysql.connect(host=data_dict['MYSQL_HOST'], user=data_dict['MYSQL_USER'],
                                           passwd=data_dict['MYSQL_PASSWD'], db=data_dict['MYSQL_DB'])
        self.cursor = self.connections.cursor()

    def save_data(self):
        """
        保存数据到mysql数据库
        :return: None
        """
        try:
            sql = 'insert into media values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ' \
                  'on duplicate key update badge=values(badge),cover=values(cover),index_show=values(index_show),' \
                  'link=values(link),folk_opera_order=values(folk_opera_order),order_type=values(order_type),' \
                  'season_id=values(season_id),is_finish=values(is_finish),' \
                  'folk_oprea_comment=values(folk_oprea_comment)'
            self.cursor.executemany(sql, self.result)
        except Exception as e:
            print('因为%e，数据写入失败！' % e)
            self.connections.rollback()
        else:
            self.connections.commit()
            if self.connections.affected_rows() > 0:
                print('%s条数据写入或者更新mysql数据库！' % len(self.result))
            self.result = []

    def judge_exist(self, folk_opera_media_id):
        """
        判断番剧是否已经在数据库中存在
        :param folk_opera_media_id:
        :return: mysql数据库查询结果
        """
        sql = r'select media_title from media where media_id = %s'
        self.cursor.execute(sql, folk_opera_media_id)
        result = self.cursor.fetchall()
        return result

    def get_data(self):
        """
        此方法获取B站番剧数据（按照播放量排序），每获取一页数据就调用对应的方法写入Mysql数据库
        :return: None
        """
        while True:
            ua = UserAgent()
            header = {}
            header['User-Agent'] = ua.random
            responses = requests.get(self.pageUrl, headers=header)
            folk_opera_data = responses.json()

            # 获取番剧数据
            for folk_oprea in folk_opera_data['data']['list']:
                media_id = folk_oprea['media_id']  # 番剧id号
                title = folk_oprea['title']  # 番剧名称
                # 已经存在的就尝试更新，因为随着时间的推移可能会出现番剧is_finish从0
                # 变为1的情况，所以所有都要获取
                badge = folk_oprea['badge']  # 是否会员专享
                cover = folk_oprea['cover']  # 番剧封面链接
                index_show = folk_oprea['index_show']  # 番剧有多少话
                link = folk_oprea['link']  # 番剧播放地址
                order = folk_oprea['order']  # 追番人数
                order_type = folk_oprea['order_type']  # 追番类型
                season_id = folk_oprea['season_id']  # 番剧属于多少季
                is_finish = folk_oprea['is_finish']  # 番剧是否完结，完结为1，未完结为0
                folk_oprea_comment = 'https://api.bilibili.com/pgc/review/short/list?media_id=' + str(
                    media_id) + '&ps=20&sort=0'
                tmp = (media_id, title, badge, cover, index_show, link, order, order_type, season_id, is_finish,
                       folk_oprea_comment)
                self.result.append(tmp)

            if self.result:  # 判断是否爬到数据
                self.save_data()  # 保存数据到mysql数据库

            # 判断有没有下一页的番剧
            if folk_opera_data['data']['has_next']:
                self.page += 1
                self.pageUrl = self.basePreUrl + str(self.page) + self.baseSuffixUrl
            else:
                print('爬取结束！')
                break
            time.sleep(random.randint(8, 16) + random.randint(8, 16) / 10)


if __name__ == "__main__":
    getFanJuData = GetFanJuData()
    getFanJuData.get_data()
