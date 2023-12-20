import json
import sys
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QTimer, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont, QColor, QTextCharFormat
from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox, QListWidgetItem, QWidget
from pyqt5_plugins.examplebutton import QtWidgets

from articleReading import ArticleReading
from lib.share import SI
from db.sql_helper import SqlHelper


class Search(QWidget):
    def __init__(self):
        super(Search, self).__init__()
        # print('加载到了')
        self.ui = uic.loadUi('./ui/search.ui')

        # print(self.ui)

        self.label_time = self.ui.label_time

        self.pushButton_search = self.ui.pushButton_search
        self.stackedWidget_select =self.ui.stackedWidget_select
        self.lineEdit_search = self.ui.lineEdit_search
        self.page_hotpot = self.ui.page_hotpot
        self.pushButton_return = self.ui.pushButton_return

        self.listWidget_hotpotarticles = self.ui.listWidget_hotpotarticles
        self.listWidget_serachresult = self.ui.listWidget_serachresult

        self.timer = QTimer()
        # print(self.timer)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)


        # 连接动作的槽函数
        self.pushButton_search.clicked.connect(self.change_searchpage)
        self.pushButton_return.clicked.connect(self.change_hotpotpage)
        self.listWidget_serachresult.itemClicked.connect(self.on_item_clicked)
        self.listWidget_hotpotarticles.itemClicked.connect(self.on_item_clicked)

        self.change_hotpotpage()



    def update_time(self):
        # 获取当前时间
        current_time = QDateTime.currentDateTime()
        # print(current_time)

        # 格式化时间字符串
        formatted_time = current_time.toString("yyyy-MM-dd HH:mm:ss")

        # 设置 QLabel 显示时间
        self.label_time.setText(formatted_time)

    def change_searchpage(self):
        print('点击了搜索按钮')
        self.stackedWidget_select.setCurrentIndex(1)
        searchContant = self.lineEdit_search.text()
        print(searchContant)
        db = SqlHelper()
        self.listWidget_serachresult.clear()
        resultsina=[]
        resultzhenjuan=[]
        with open('shared_data.json', 'r') as file:
            data = json.load(file)
        # print(data[0]['permission'][0])
        # print(data[0]['permission'][0]=='1')
        if data[0]['permission'][0]=='1':
            resultsina = db.get_list('select * from sina_crawler_nationalNews where title like %s UNION select * from sina_crawler_LocalNews where title like %s UNION select * from sina_crawler_InternationalNews where title like %s ', [f'%{searchContant}%']*3)
            print(resultsina)
        if data[0]['permission'][1] == '1':
            resultzhenjuan = db.get_list('select * from crawler_tb4 where title like %s UNION select * from crawler_tb3 where title like %s UNION select * from crawler_tb2 where title like %s UNION select * from crawler_tb1 where title like %s;', [f'%{searchContant}%']*4)
            print(resultzhenjuan)
        result=resultsina+resultzhenjuan
        # print(result)
        i=1
        font = QFont("Arial", 12)  # 设置字体为Arial，大小为12
        text_color = QColor(255, 0, 0)  # 设置文本颜色为红色
        for new in result:
            item = QListWidgetItem(f'{i}:{new["title"]}')

            # 创建 QTextCharFormat 对象
            char_format = QTextCharFormat()

            # 设置文字颜色为红色
            char_format.setForeground(QColor(255, 0, 0))

            # 设置格式应用于指定范围的文本
            item.setData(Qt.TextColorRole, char_format)

            self.listWidget_serachresult.addItem(item)
            i += 1


    def change_hotpotpage(self):
        self.stackedWidget_select.setCurrentIndex(0)
        db = SqlHelper()
        result = db.get_list('select * from sina_crawler_nationalNews',[])
        for new in result:
            item = QListWidgetItem(f'{new["id"]}:{new["title"]}')
            self.listWidget_hotpotarticles.addItem(item)

    def on_item_clicked(self,item):
        print(item.text())
        SI.article_reading_page = ArticleReading(item.text())
        SI.article_reading_page.ui.show()
        self.ui.hide()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Search()
    SI.page1.ui.show()
    sys.exit(app.exec_())
