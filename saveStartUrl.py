import pymysql
from Bzhan_comments import settings


class SaveStartUrl(object):
    def __init__(self):
        self.result = [] # 用来保存读取的爬取路径的数据
        # 初始化mysql链接
        self.connections = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DB)
        self.cursor = self.connections.cursor()

    def getStartUrlData(self, startUrlPath):
        """
        从输入的文本路径中读取爬取过的url数据
        :param startUrlPath:文本文件的路径
        :return result:None
        """
        try:
            with open(startUrlPath, 'r', encoding='utf8') as f:
                data = f.readlines()
                for line in data:
                    media_id = line.split('media_id=')[-1].split('&')[0]
                    self.result.append((line, media_id))
        except Exception as identifier:
            print('因为%s数据读取失败！' % identifier)
        self.saveData()

    def saveData(self):
        """
        将result里面保存的数据写入到mysql数据库中
        :param None
        :return None
        """
        if self.result:
            try:
                sql = 'insert ignore into comment_url values(%s, %s)'
                self.cursor.executemany(sql, self.result)
            except Exception as identifier:
                print('因为%s数据写入mysql数据库失败！进行回滚操作！' % identifier)
                self.connections.rollback()
            else:
                self.connections.commit()
                print('%s条数据已写入mysql数据库！' % self.connections.affected_rows())
            finally:
                self.connections.close()
        else:
            print('未读取到相关的数据，请检查文本路径是否正确！')


if __name__ == "__main__":
    saveStartUrl = SaveStartUrl()
    saveStartUrl.getStartUrlData('startUrl.txt')
