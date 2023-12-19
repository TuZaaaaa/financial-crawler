import sys
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont, QColor
from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox, QListWidgetItem
from pyqt5_plugins.examplebutton import QtWidgets
from lib.share import SI
from db.sql_helper import SqlHelper


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

        self.page_main = self.ui.page_main
        self.page_wordAnalysis = self.ui.page_wordAnalysis
        self.page_stock = self.ui.page_stock

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
        self.action_modifysina.triggered.connect(self.modify_sina)
        self.action_modifyzhenjuan.triggered.connect(self.modify_zhenjuan)
        self.listWidget.itemClicked.connect(self.switch_page)
        self.pushButton_search.clicked.connect(self.change_searchpage)
        self.pushButton_return.clicked.connect(self.change_hotpotpage)

        self.change_hotpotpage()

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

    def switch_page(self,item):
        index = self.listWidget.row(item)
        print(index)
        self.stackedWidget.setCurrentIndex(index)

    def update_time(self):
        # 获取当前时间
        current_time = QDateTime.currentDateTime()

        # 格式化时间字符串
        formatted_time = current_time.toString("yyyy-MM-dd HH:mm:ss")

        # 设置 QLabel 显示时间
        self.label_time.setText(formatted_time)

    def change_searchpage(self):
        self.stackedWidget_select.setCurrentIndex(1)
        searchContant = self.lineEdit_search.text()
        print(searchContant)
        db = SqlHelper()
        result = db.get_list('select * from sina_crawler_nationalNews where title like %s UNION select * from sina_crawler_LocalNews where title like %s UNION select * from sina_crawler_InternationalNews where title like %s UNION select * from crawler_tb4 where title like %s UNION select * from crawler_tb3 where title like %s UNION select * from crawler_tb2 where title like %s UNION select * from crawler_tb1 where title like %s;', [f'%{searchContant}%']*7)
        print(result)
        i=1
        font = QFont("Arial", 12)  # 设置字体为Arial，大小为12
        text_color = QColor(255, 0, 0)  # 设置文本颜色为红色
        for new in result:
            item = QListWidgetItem(f'{i}:{new["title"]}')
            self.listWidget_serachresult.addItem(item)
            i+=1


    def change_hotpotpage(self):
        self.stackedWidget_select.setCurrentIndex(0)
        db = SqlHelper()
        result = db.get_list('select * from sina_crawler_nationalNews',[])
        for new in result:
            item = QListWidgetItem(f'{new["id"]}:{new["title"]}')
            self.listWidget_hotpotarticles.addItem(item)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Main()
    SI.page1.ui.show()
    sys.exit(app.exec_())
