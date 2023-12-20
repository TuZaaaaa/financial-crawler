import os
import sys

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class WordCloudGenerate:

    def __init__(self, datasource, save_path):
        """
        词云生成
        :param datasource: 数据源 str
        :param save_path: 保存路径 str
        """
        self.datasource = datasource
        self.save_path = save_path

    @staticmethod
    def get_stopword_list(file):
        with open(file, 'r', encoding='utf-8') as f:
            stopword_list = [word.strip('\n') for word in f.readlines()]
        return stopword_list

    @staticmethod
    def pre_process(text, stopword_list):
        print('pre_process')
        # 分词
        seg_list = jieba.cut(text)
        return [w for w in seg_list if w not in stopword_list]

    def word_cloud_generate(self, word_list):
        # 创建词云对象
        wordcloud = WordCloud(font_path=os.path.join(os.path.dirname(__file__), './font/fzht.TTF'), width=800, height=400, background_color='white').generate(
            " ".join(word_list))

        # 显示词云图像
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(self.save_path, format='png')
        plt.show()

    def run(self):
        print(sys.path[0])
        # 预处理
        # 读取停用词列表
        stopword_list = self.get_stopword_list(os.path.join(os.path.dirname(__file__) + './words/cn_stopwords.txt'))
        word_list = self.pre_process(self.datasource, stopword_list)
        # 词云生成
        self.word_cloud_generate(word_list)
        return 1
    def getlist(self):
        print(sys.path[0])
        # 预处理
        # 读取停用词列表
        stopword_list = self.get_stopword_list(os.path.join(os.path.dirname(__file__) + './words/cn_stopwords.txt'))
        word_list = self.pre_process(self.datasource, stopword_list)
        # 词云生成
        return word_list

