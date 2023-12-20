import json
import sys
import time

from PyQt5 import uic
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtWidgets import QMessageBox
from pyqt5_plugins.examplebutton import QtWidgets

import search
import word_analysis
from db.sql_helper import SqlHelper
from lib.share import SI
from stock_table_crawler import StockTableCrawler
from word_analysis import Word_analysis
from word_cloud_generate import WordCloudGenerate


class Main():
    def __init__(self):
        super(Main, self).__init__()
        self.ui = uic.loadUi('./ui/main.ui')
        with open('shared_data.json', 'r') as file:
            data = json.load(file)
        print(data)
        self.user = data
        self.permission=self.user[0]['permission']
        print(self.permission)



        self.menu_sina = self.ui.menu_sina
        self.menu_zhenjuan = self.ui.menu_zhenjuan
        # 获取菜单的动作
        self.action_modifysina = self.ui.action_modifysina
        self.action_modifyzhenjuan = self.ui.action_modifyzhenjuan

        self.listWidget = self.ui.listWidget
        self.stackedWidget = self.ui.stackedWidget


        self.search_page = search.Search()
        self.word_analysis_page = Word_analysis()
        self.stock_table_page = StockTableCrawler()

        # 将 Search 页面添加到 stackedWidget
        self.stackedWidget.addWidget(self.search_page.ui)
        self.stackedWidget.addWidget(self.word_analysis_page.ui)
        self.stackedWidget.addWidget(self.stock_table_page.ui)



        self.listWidget.itemClicked.connect(self.switch_page)
        self.action_modifysina.triggered.connect(self.modify_sina)
        self.action_modifyzhenjuan.triggered.connect(self.modify_zhenjuan)

        self.initpermission()

    def initpermission(self):

        if self.permission[0]!='1':
            self.menu_sina.setTitle("新浪×")
            self.action_modifysina.setText('启用')
        if self.permission[1]!='1':
            self.menu_zhenjuan.setTitle("中国证券网×")
            self.action_modifyzhenjuan.setText('启用')

    def modify_sina(self):
        # print('禁用新浪')
        # print(self.menu_sina.title())
        # print(self.permission)
        db = SqlHelper()
        if self.menu_sina.title()=='新浪√':
            self.menu_sina.setTitle("新浪×")
            self.action_modifysina.setText('启用')
            # print(self.user)
            self.permission = '0' + self.permission[1:]
            # print(self.permission)
            get_word_analysis_picture()
            QMessageBox.information(self.ui, '新浪源', '新浪源关闭', QMessageBox.Yes)



        else:
            self.menu_sina.setTitle("新浪√")
            self.action_modifysina.setText('禁用')
            # print(self.permission[0])
            self.permission = '1' + self.permission[1:]
            # print(self.permission)
            get_word_analysis_picture()
            QMessageBox.information(self.ui, '新浪源', '新浪源开启', QMessageBox.Yes)

        self.user[0]['permission'] = self.permission
        with open('shared_data.json', 'w') as file:
            json.dump(self.user, file)
        db.modify('update user set permission=%s where id =%s', (self.permission,self.user[0]['id']))

    def modify_zhenjuan(self):
        # print('禁用中国证券网')
        db = SqlHelper()
        if self.menu_zhenjuan.title()=='中国证券网√':
            self.menu_zhenjuan.setTitle("中国证券网×")
            self.action_modifyzhenjuan.setText('启用')
            self.permission = self.permission[:1]+ '0'
            get_word_analysis_picture()
            QMessageBox.information(self.ui, '中国证券网源', '中国证券网源关闭', QMessageBox.Yes)
        else:
            self.menu_zhenjuan.setTitle("中国证券网√")
            self.action_modifyzhenjuan.setText('禁用')
            self.permission = self.permission[:1] + '1'
            get_word_analysis_picture()
            QMessageBox.information(self.ui, '中国证券网源', '中国证券网源开启', QMessageBox.Yes)
        db.modify('update user set permission=%s where id =%s', (self.permission, self.user[0]['id']))


    def switch_page(self, item):
        self.refresh_current_page()
        QCoreApplication.processEvents()  # 处理事件队列，确保刷新完成
        index = self.listWidget.row(item)
        self.stackedWidget.setCurrentIndex(index)

    def load_page(self, ui_file):
        page = uic.loadUi(ui_file)
        self.stackedWidget.addWidget(page)

    def refresh_current_page(self):
        # 刷新当前页面
        current_widget = self.stackedWidget.currentWidget()
        current_widget.repaint()
        current_widget.update()
        

def get_word_analysis_picture():
    db = SqlHelper()
    resultsina = []
    resultzhenjuan = []
    with open('shared_data.json', 'r') as file:
        data = json.load(file)
    if data[0]['permission'][0] == '1':
        resultsina = db.get_list(
            'select * from sina_crawler_nationalNews UNION select * from sina_crawler_LocalNews UNION select * from sina_crawler_InternationalNews  ',
            [])
    if data[0]['permission'][1] == '1':
        resultzhenjuan = db.get_list(
            'select * from crawler_tb4  UNION select * from crawler_tb3  UNION select * from crawler_tb2   UNION select * from crawler_tb1  ;',
            [])
    result = resultsina + resultzhenjuan
    print(result)
    contents = ''
    for r in result:
        contents += r['content']
    print(contents)
    try:
        wcg = WordCloudGenerate(contents, 'picture/wordcloud.png')
        result = wcg.run()
        print(result)
        # word_analysisObejct = Word_analysis()
        # time.sleep(2)
        # word_analysisObejct.init_picture()

    except Exception as e:
        print(e)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Main()

    SI.page1.ui.show()
    sys.exit(app.exec_())
