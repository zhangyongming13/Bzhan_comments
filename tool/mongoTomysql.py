import pymongo
import pymysql
# pycharm误报不用处理
from GetDataFromEnv import get_data_from_env


class mongoTomysql():
    def __init__(self):
        # 初始化mongodb连接并返回
        data_dict = get_data_from_env()
        mongoHost = data_dict['MONGODB_HOST']
        mongoport = int(data_dict['MONGODB_PORT'])
        mongoDbname = data_dict['MONGODB_DBNAME']
        mongoAuthDb = data_dict['MONGODB_AUTHDB']
        mongoUser = data_dict['MONGODB_USER']
        mongoPasswd = data_dict['MONGODB_PASSWD']
        mongoSheetname = data_dict['MONGODB_SHEETNAME_1']
        mongo_client = pymongo.MongoClient(host=mongoHost, port=mongoport)
        mongo_db = mongo_client[mongoAuthDb]
        mongo_db.authenticate(mongoUser, mongoPasswd)
        mongo_db = mongo_client[mongoDbname]
        self.mongo_object = mongo_db[mongoSheetname]

    def getDataformongo(self):
        """
        读取mongodb中的数据
        :return: 返回读取到的数据
        """
        data = self.mongo_object.find()
        return data

    def saveDatatomysql(self):
        data = self.getDataformongo()
        dataList = []
        for i in data:
            # executemany()需要处理的数据参数是一个列表，列表每个中每一个元素必须是元组tuple
            # 例如：  [(1,'小明'),(2,'zeke'),(3,'琦琦'),(4,'韩梅梅')]
            temp = (i['comment_mid'], i['media_id'], i['comment_author_mid'], i['comment_author_avatar'],
                    i['comment_author_name'], i['comment_date'], i['comment_text'], i['score'],
                    i['comment_likes'], i['comment_disliked'], i['comment_liked'], i['last_index_show'])
            dataList.append(temp)
        print('%s条数据即将写入mysql数据库！' % len(dataList))
        # 初始化mysql连接并返回
        data_dict = get_data_from_env()
        mysqlHost = data_dict['MYSQL_HOST']
        mysqlUser = data_dict['MYSQL_USER']
        mysqlPasswd = data_dict['MYSQL_PASSWD']
        mysqlDb = data_dict['MYSQL_DB']
        connection = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPasswd, db=mysqlDb)
        cursor = connection.cursor()
        try:
            cursor.executemany(r'insert ignore into bzhan_comment values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', dataList)
        except Exception as e:
            print('因为%s评论数据写入mysql数据库失败！数据库进行回滚操作' % e)
            # 回滚数据库
            connection.rollback()
        else:
            connection.commit()
            if connection.affected_rows() > 0:
                print('%d行评论数据写入mysql成功！' % len(dataList))
            # 进行mongo数据删除
            try:
                self.mongo_object.drop()
            except Exception as e:
                print('因为%s mongo数据库内数据删除失败！' % e)
            else:
                print('mongo数据库内数据删除成功！')
        finally:
            connection.close()


if __name__ == '__main__':
    mongoTomysql = mongoTomysql()
    mongoTomysql.saveDatatomysql()
