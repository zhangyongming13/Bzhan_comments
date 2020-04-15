import pymysql
from Bzhan_comments import settings


# 从文本文件中读取media_name和media_id数据并写入mysql数据库
class SaveNameMediaIdToMysql():
    def __init__(self):
        # 初始化mysql连接并返回
        mysqlHost = settings.MYSQL_HOST
        mysqlUser = settings.MYSQL_USER
        mysqlPasswd = settings.MYSQL_PASSWD
        mysqlDb = settings.MYSQL_DB
        self.connection = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPasswd, db=mysqlDb)
        self.cursor = self.connection.cursor()

        self.data = []

    def get_data(self, file_path):
        with open(file_path, 'r', encoding='utf8') as f:
            datas = f.read().split('\n')[:-1]
        for data in datas:
            name = data.split('https')[0].strip(' ')
            media_id = int(data.split('media_id=')[-1].split('&')[0])
            temp = (media_id, name)
            self.data.append(temp)

    def sava_to_mysql(self):
        try:
            self.cursor.executemany(r'insert into media values(%s, %s)', self.data)
            self.connection.commit()
            print('写入成功！')
        except Exception as e:
            print('因为%s保存到数据库失败，进行回滚操作！' % e)
            self.connection.rollback()
        finally:
            self.connection.close()


if __name__ == '__main__':
    savenamemediaidmysql = SaveNameMediaIdToMysql()
    savenamemediaidmysql.get_data('爬取.txt')
    savenamemediaidmysql.sava_to_mysql()
