import json
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import sinaCrawler
from db.sql_helper import SqlHelper
from lib.share import SI
from main import Main
from stock_crawler import StockCrawler


class WorkThread(QThread):
    data_fetched_signal = pyqtSignal()

    def run(self):
        print('run')
        Login.update_data()
        self.data_fetched_signal.emit()


class Login:

    def __init__(self):
        self.ui = uic.loadUi('./ui/login.ui')
        self.sql_helper = SqlHelper()
        icon = QIcon('image/logo.png')  # 替换为你的图标文件的路径
        self.ui.setWindowIcon(icon)
        self.ui.setWindowTitle('财经新闻信息抓取与分析系统')

        # 登录
        self.ui.pushButton_login.clicked.connect(self.login)

        self.worker_thread = None  # 初始化时不创建线程

    def login(self):
        print('login')
        name = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        result = self.sql_helper.get_list('select * from user where name = %s and password = %s', [name, password])
        print(result)
        if len(result) == 0:
            QMessageBox.warning(self.ui, '登录失败', '用户名或密码错误', QMessageBox.Yes)
        else:
            # print(result[0]['permission'])
            # 将数据写入 JSON 文件
            with open('shared_data.json', 'w') as file:
                json.dump(result, file)
            if self.ui.radioButton_update.isChecked():
                self.start_update()
            else:
                SI.main_page = Main()
                SI.main_page.ui.show()
                self.ui.hide()

    def start_update(self):
        if self.worker_thread is None:
            self.worker_thread = WorkThread()
        if not self.worker_thread.isRunning():
            # 添加 loading 显示
            self.ui.label_update.setText('数据库更新中...')
            self.worker_thread.data_fetched_signal.connect(self.on_data_fetched)
            self.worker_thread.start()

    @staticmethod
    def update_data():
        # 爬虫加载
        res = sinaCrawler.run()
        sc = StockCrawler()
        res2 = sc.run()
    def on_data_fetched(self):
        SI.main_page = Main()
        SI.main_page.ui.show()
        self.ui.hide()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Login()
    SI.page1.ui.show()
    app.exec()
