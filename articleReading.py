import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton
from pyqt5_plugins.examplebutton import QtWidgets

from db.sql_helper import SqlHelper
from lib.share import SI



class ArticleReading():
    def __init__(self,title):
        self.ui = uic.loadUi('./ui/article_reading.ui')
        result_list = title.split(":", 1)
        self.seachtitle = result_list[1].strip()
        print(self.seachtitle)
        self.getArticle()
        self.articleObject = self.getArticle()
        self.pushButton = self.ui.pushButton


        try:
            self.label_title = self.ui.label_title
            self.textBrowser_body = self.ui.textBrowser_body
            self.label_time = self.ui.label_time
        except Exception as e:
            print(e)
        self.pushButton.clicked.connect(self.return_main_page)
        self.initpage()



    def getArticle(self):
        db = SqlHelper()
        result=db.get_one('''
        select * from sina_crawler_nationalNews where title = %s
        UNION select * from sina_crawler_LocalNews where title = %s
        UNION select * from sina_crawler_InternationalNews where title = %s
        UNION select * from crawler_tb4 where title = %s
        UNION select * from crawler_tb3 where title = %s
        UNION select * from crawler_tb2 where title = %s 
        UNION select * from crawler_tb1 where title = %s;
        ''',[self.seachtitle]*7)

        return result

    def initpage(self):
        try:
            self.label_title.setText(self.articleObject['title'])
            # 定义格式化字符串
            date_format = "%Y-%m-%d %H:%M:%S"
            self.label_time.setText(self.articleObject['time'].strftime(date_format))
            self.textBrowser_body.setWordWrapMode(1)
            self.textBrowser_body.setPlainText(self.articleObject['content'])
        except Exception as e:
            print(e)

    def return_main_page(self):
        # 在窗口关闭时创建并显示第二个页面
        from main import Main
        try:
            SI.main_page = Main()
            SI.main_page.ui.show()
            self.ui.hide()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = ArticleReading()
    SI.page1.ui.show()
    app.exec()