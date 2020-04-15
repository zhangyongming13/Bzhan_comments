import pymongo
import pymysql
import jieba
import numpy
import math
from Bzhan_comments import settings
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


class Analycis():
    def __init__(self):
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        db_name = settings.MONGODB_DBNAME
        sheet_name_1 = settings.MONGODB_SHEETNAME_1
        sheet_name_2 = settings.MONGODB_SHEETNAME_2
        sheet_name_3 = settings.MONGODB_SHEETNAME_3

        # 初始化mongodb连接并返回
        mongo_client = pymongo.MongoClient(host=host, port=port)
        mongo_db = mongo_client[db_name]
        self.mongo_object_1 = mongo_db[sheet_name_1]
        self.mongo_object_2 = mongo_db[sheet_name_2]
        self.mongo_object_3 = mongo_db[sheet_name_3]

        # 初始化mysql连接并返回
        mysqlHost = settings.MYSQL_HOST
        mysqlUser = settings.MYSQL_USER
        mysqlPasswd = settings.MYSQL_PASSWD
        mysqlDb = settings.MYSQL_DB
        self.connection = pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPasswd, db=mysqlDb)
        self.cursor = self.connection.cursor()

    # 从数据库中获取番剧已经爬取的评论
    def get_data(self, media_id):
        data = ''
        sql = "select comment_text from bzhan_comment where media_id = %s" % (media_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for i in result:
            data += str(i[0]) + '。'
        return data

    # 从分词文件中加载分词
    def load_stopwords(self):
        filepath = 'chineseStopWords.txt'
        stopwords = []
        with open(filepath, 'r', encoding='utf8') as f:
            for word in f:
                stopwords.append(word.strip())
        return stopwords

    # 图片大小不一样的时候以image2为准，对image1裁剪
    def imageOverlay(self, image1, image2):
        result = image2
        image1 = Image.open(image1)
        image2 = Image.open(image2)
        # 进行裁剪操作
        image1 = image1.resize((image2.width, image2.height), Image.ANTIALIAS)
        # 进行两张图片的叠加
        newImage = Image.blend(image1, image2, (math.sqrt(5) - 1) / 2)
        newImage.save(result)


    # 生成词云并保存到本地
    def get_comments_wordcloud(self):
        print('请输入需要生产词云的番剧名称：')
        while True:
            fanOperaname = str(input())
            sql = "select media_id from media where media_name = '%s'" % (fanOperaname)
            self.cursor.execute(sql)
            temp = self.cursor.fetchall()
            if len(temp) != 0:
                result = temp[0][0]
                break
            else:
                print('输入番剧名称有错，请重新输入：')
        image_path = '词云相关数据/' + str(fanOperaname) + '.jpeg'
        data = self.get_data(result)

        # 用jieba进行精确分词，返回list
        data = jieba.lcut(data, cut_all=False)
        text = '。'.join(data)

        # 加载停止词
        stop_words = self.load_stopwords()

        # 中文的话要设置中文字体，不然词云会乱码
        font_path = 'SourceHanSansCN-Regular.ttf'
        # 设置词云背景图
        background_image = numpy.array(Image.open(image_path))
        # 从背景图中取色，不同区域字不同颜色
        img_colors = ImageColorGenerator(background_image)
        stopwords = set(stop_words)

        wc = WordCloud(
            font_path=font_path,
            margin=2,
            mask=background_image,
            scale=2,
            max_words=400,
            min_font_size=4,
            stopwords=stopwords,
            random_state=42,
            background_color='white',
            max_font_size=100,
        )
        wc.generate(text)  # 生成词云

        # 获取文本排序
        process_word = WordCloud.process_text(wc,text)
        sort = sorted(process_word.items(), key=lambda e:e[1], reverse=True)
        print(sort[:50])
        wc.recolor(color_func=img_colors)

        ciyun_image = str(image_path.split('.')[0] + '.png')

        wc.to_file(ciyun_image)

        # 将词云图片和原图片进行叠加操作
        self.imageOverlay(image_path, ciyun_image)
        return True


if __name__ == '__main__':
    analycis = Analycis()
    analycis.get_comments_wordcloud()
