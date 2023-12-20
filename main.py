import json
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from pyqt5_plugins.examplebutton import QtWidgets

import search
from db.sql_helper import SqlHelper
from lib.share import SI
from stock_table_crawler import StockTableCrawler


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
        self.stock_table_page = StockTableCrawler()

        # 将 Search 页面添加到 stackedWidget
        self.stackedWidget.addWidget(self.search_page.ui)
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
            QMessageBox.information(self.ui, '新浪源', '新浪源关闭', QMessageBox.Yes)



        else:
            self.menu_sina.setTitle("新浪√")
            self.action_modifysina.setText('禁用')
            # print(self.permission[0])
            self.permission = '1' + self.permission[1:]
            # print(self.permission)
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
            QMessageBox.information(self.ui, '中国证券网源', '中国证券网源关闭', QMessageBox.Yes)
        else:
            self.menu_zhenjuan.setTitle("中国证券网√")
            self.action_modifyzhenjuan.setText('禁用')
            self.permission = self.permission[:1] + '1'
            QMessageBox.information(self.ui, '中国证券网源', '中国证券网源开启', QMessageBox.Yes)
        db.modify('update user set permission=%s where id =%s', (self.permission, self.user[0]['id']))


    def switch_page(self, item):
        index = self.listWidget.row(item)
        # print(index)
        self.stackedWidget.setCurrentIndex(index)

    def load_page(self, ui_file):
        page = uic.loadUi(ui_file)
        self.stackedWidget.addWidget(page)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Main()

    SI.page1.ui.show()
    sys.exit(app.exec_())
