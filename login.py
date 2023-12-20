import json
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

from db.sql_helper import SqlHelper
from lib.share import SI
from main import Main


class Login:

    def __init__(self):
        self.ui = uic.loadUi('./ui/login.ui')
        self.sql_helper = SqlHelper()

        # 登录
        self.ui.pushButton_login.clicked.connect(self.login)

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
            SI.main_page = Main()
            SI.main_page.ui.show()
            self.ui.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Login()
    SI.page1.ui.show()
    app.exec()
