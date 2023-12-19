import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from pyqt5_plugins.examplebutton import QtWidgets

import search
from lib.share import SI
from stock_table_crawler import StockTableCrawler


class Main():
    def __init__(self):
        super(Main, self).__init__()
        self.ui = uic.loadUi('./ui/main.ui')

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


    def modify_sina(self):
        print('禁用新浪')
        # print(self.menu_sina.title())
        if self.menu_sina.title()=='新浪√':
            self.menu_sina.setTitle("新浪×")
            self.action_modifysina.setText('启用')
            QMessageBox.information(self.ui, '新浪源', '新浪源关闭', QMessageBox.Yes)
        else:
            self.menu_sina.setTitle("新浪√")
            self.action_modifysina.setText('禁用')
            QMessageBox.information(self.ui, '新浪源', '新浪源开启', QMessageBox.Yes)

    def modify_zhenjuan(self):
        print('禁用中国证券网')
        if self.menu_zhenjuan.title()=='中国证券网√':
            self.menu_zhenjuan.setTitle("中国证券网×")
            self.action_modifyzhenjuan.setText('启用')
            QMessageBox.information(self.ui, '中国证券网源', '中国证券网源关闭', QMessageBox.Yes)
        else:
            self.menu_zhenjuan.setTitle("中国证券网√")
            self.action_modifyzhenjuan.setText('禁用')
            QMessageBox.information(self.ui, '中国证券网源', '中国证券网源开启', QMessageBox.Yes)

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
