from db.sql_helper import SqlHelper
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

db = SqlHelper()


def get_stopword_list(file):
    with open(file, 'r', encoding='utf-8') as f:
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list


def query_data():
    print('query_data')
    return db.get_list('select * from crawler_tb1', [])


def pre_process(text, stopword_list):
    print('pre_process')
    # 分词
    seg_list = jieba.cut(text)
    return [w for w in seg_list if w not in stopword_list]


def word_cloud_generate(word_list):
    # 创建词云对象
    wordcloud = WordCloud(font_path='./font/fzht.TTF', width=800, height=400, background_color='white').generate(
        " ".join(word_list))

    # 显示词云图像
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud.png', format='png')
    plt.show()


if __name__ == '__main__':
    print('analyze')
    # 查询数据
    contents = ''
    text = query_data()
    for t in text:
        contents += t['content']
    print(contents)
    # 预处理
    # 读取停用词列表
    stopword_list = get_stopword_list('./words/cn_stopwords.txt')
    word_list = pre_process(contents, stopword_list)
    # 词云生成
    word_cloud_generate(word_list)
