from Bzhan_comments import settings
import pymongo
import jieba


class Analycis():
    def __init__(self):
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        db_name = settings.MONGODB_DBNAME
        sheet_name = settings.MONGODB_SHEETNAME

        # 初始化mongodb连接并返回
        mongo_client = pymongo.MongoClient(host=host, port=port)
        mongo_db = mongo_client[db_name]
        self.mongo_object = mongo_db[sheet_name]

    def get_data(self, field):
        data = ''
        data_gen = self.mongo_object.find({}, {'_id':0, field:1})
        for i in data_gen:
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

    def get_comments_wordcloud(self):
        data = self.get_data('comment_text')

        # 用jieba进行精确分词，返回list
        data = jieba.lcut(data, cut_all=False)
        text = ' '.join(data)

        # 去除停止词
        stop_words = self.load_stopwords()
        move_stopwords_text = ''
        for word in text:
            if word not in stop_words:
                if word != '\t' and '\n':
                    move_stopwords_text += word
        pass

if __name__ == '__main__':
    analycis = Analycis()
    analycis.get_comments_wordcloud()
