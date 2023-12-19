import sys

from PyQt5 import uic
from pyqt5_plugins.examplebutton import QtWidgets

from lib.share import SI


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

        self.load_page('./ui/search.ui')
        self.load_page('./ui/login.ui')
        self.load_page("./ui/search.ui")
        self.listWidget.itemClicked.connect(self.switch_page)

    def switch_page(self, item):
        index = self.listWidget.row(item)
        print(index)
        self.stackedWidget.setCurrentIndex(index)

    def load_page(self, ui_file):
        page = uic.loadUi(ui_file)
        self.stackedWidget.addWidget(page)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Main()
    SI.page1.ui.show()
    sys.exit(app.exec_())
