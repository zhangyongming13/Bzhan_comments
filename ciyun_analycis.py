import pymongo
import jieba
import numpy
from Bzhan_comments import settings
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


image_path = 'timg.jpeg'


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

    # 从数据库中获取番剧已经爬取的评论
    def get_data(self, field):
        data = ''
        data_gen_3 = self.mongo_object_3.find({}, {'_id':0, field:1})
        for i in data_gen_3:
            data += i['comment_text'] + '。'
        return data

    # 从分词文件中加载分词
    def load_stopwords(self):
        filepath = 'chineseStopWords.txt'
        stopwords = []
        with open(filepath, 'r', encoding='utf8') as f:
            for word in f:
                stopwords.append(word.strip())
        return stopwords

    # 生成词云并保存到本地
    def get_comments_wordcloud(self):
        data = self.get_data('comment_text')

        # 用jieba进行精确分词，返回list
        data = jieba.lcut(data, cut_all=False)
        text = ' '.join(data)

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

        ciyun_image = image_path.split('.')[0] + '.png'

        wc.to_file(ciyun_image)
        return True


if __name__ == '__main__':
    analycis = Analycis()
    analycis.get_comments_wordcloud()
