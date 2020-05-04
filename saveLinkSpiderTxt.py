import pymysql
from Bzhan_comments import settings


class saveLinkSpiderTxt(object):
    def __init__(self):
        # 初始化mysql链接
        self.connections = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DB)
        self.cursor = self.connections.cursor()
        self.linkDatas = None

    def getLinkData(self):
        """
        从meida表中获取还没有爬取过comment的番剧title和comment入口链接
        :param:None
        :return:None
        """
        sql = "SELECT m.media_title, m.folk_oprea_comment FROM media m WHERE m.media_id NOT IN ( SELECT media_id FROM bzhan_comment ) AND m.is_finish = 1"
        self.cursor.execute(sql)
        self.linkDatas = self.cursor.fetchall()

    def saveDatas(self):
        """
        将获取到的未爬取番剧的数据（title和comment入口url）写入到爬取.txt中，方便爬取。
        :param:None
        :return:None
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
    save_link_spider_txt = saveLinkSpiderTxt()
    save_link_spider_txt.getLinkData()
    save_link_spider_txt.saveDatas()
