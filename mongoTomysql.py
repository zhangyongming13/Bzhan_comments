import pymongo
import pymysql
from Bzhan_comments import settings


class mongoTomysql():
    def __init__(self):
        # 初始化mongodb连接并返回
        mongoHost = settings.MONGODB_HOST
        mongoport = settings.MONGODB_PORT
        mongoDbname = settings.MONGODB_DBNAME
        mongoSheetname = settings.MONGODB_SHEETNAME_1
        mongo_client = pymongo.MongoClient(host=mongoHost, port=mongoport)
        mongo_db = mongo_client[mongoDbname]
        self.mongo_object = mongo_db[mongoSheetname]

        # 初始化mysql连接并返回
        mysqlHost = settings.MYSQL_HOST
        mysqlUser = settings.MYSQL_USER
        mysqlPasswd= settings.MYSQL_PASSWD
        mysqlDb = settings.MYSQL_DB
        self.connection = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPasswd, db=mysqlDb)
        self.cursor = self.connection.cursor()

    def getDataformongo(self):
        data = self.mongo_object.find()
        return data

    def saveDatatomysql(self):
        data = self.getDataformongo()
        dataList = []
        commentMidlist = []
        mediaIdlist = []
        for i in data:
            if i['comment_mid'] in commentMidlist and i['media_id'] in mediaIdlist:
                print(str(i['comment_mid']) + '该评论重复，取消重复写入！')
            else:
                # executemany()需要处理的数据参数是一个列表，列表每个中每一个元素必须是元组tuple
                # 例如：  [(1,'小明'),(2,'zeke'),(3,'琦琦'),(4,'韩梅梅')]
                temp = (i['comment_mid'], i['media_id'], i['comment_author_mid'], i['comment_author_avatar'],
                        i['comment_author_name'], i['comment_date'], i['comment_text'], i['score'],
                        i['comment_likes'], i['comment_disliked'], i['comment_liked'], i['last_index_show'])
                dataList.append(temp)
                commentMidlist.append(i['comment_mid'])
                mediaIdlist.append(i['media_id'])
        print('%s条数据即将写入mysql数据库！' % len(dataList))
        try:
            self.cursor.executemany(r'insert into bzhan_comment values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', dataList)
        except Exception as e:
            print('因为%s评论数据写入mysql数据库失败！数据库进行回滚操作' % e)
            # 回滚数据库
            self.connection.rollback()
        else:
            self.connection.commit()
            print('评论数据写入mysql成功！')
        finally:
            self.connection.close()
        # 进行mongo数据删除
        try:
            self.mongo_object.drop()
        except Exception as e:
            print('因为%s mongo数据库内数据删除失败！' % e)
        else:
            print('mongo数据库内数据删除成功！')


if __name__ == '__main__':
    mongoTomysql = mongoTomysql()
    mongoTomysql.saveDatatomysql()
