import pymysql
from Bzhan_comments import settings


class saveLinkSpiderTxt(object):
    def __init__(self):
        # 初始化mysql链接
        self.connections = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                                           passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DB)
        self.cursor = self.connections.cursor()
        self.linkDatas = None

    def getLinkData(self, spider_flag):
        """
        从meida表中获取番剧title和comment入口链接，参数spider_flag的作用是选择所有番剧爬取
        一次（旧的番剧可能更新评论）还是只爬取没有爬取过的番剧评论
        :param spider_flag:控制全部爬取还是部分爬取
        :return:None
        """
        if spider_flag == 'y':
            sql = "SELECT m.media_title, m.folk_oprea_comment FROM media m WHERE m.is_finish = 1"
        else:
            sql = "SELECT m.media_title, m.folk_oprea_comment FROM media m WHERE m.media_id NOT IN " \
                  "( SELECT media_id FROM bzhan_comment ) AND m.is_finish = 1"
        self.cursor.execute(sql)
        self.linkDatas = self.cursor.fetchall()

    def saveDatas(self):
        """
        将获取到的未爬取番剧的数据（title和comment入口url）写入到爬取.txt中，方便爬取。
        :return: None
        """
        if self.linkDatas:
            tmp = []
            for linkdata in self.linkDatas:
                tmp.append(' '.join(linkdata))
                tmp.append('\n')
            with open(settings.SPIDER_TEXT, 'a', encoding='utf8') as f:
                f.writelines(tmp)
        else:
            print('media表中没有待爬取的番剧！')


if __name__ == "__main__":
    spider_flag = input('请选择全部番剧重新爬取还是只爬取没有爬取过的番剧！y全部爬取，n部分爬取！')
    while spider_flag != 'y' and spider_flag != 'n':
        spider_flag = input('请输入y或者n')
    save_link_spider_txt = saveLinkSpiderTxt()
    save_link_spider_txt.getLinkData(spider_flag)
    save_link_spider_txt.saveDatas()
