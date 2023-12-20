import sys

from PyQt5.QtGui import QPixmap
from pyqt5_plugins.examplebutton import QtWidgets
from qtpy import uic

from db.sql_helper import SqlHelper
from lib.share import SI
from word_detailed_table import Word_detailed_table


class Word_analysis():

    def __init__(self):
        self.ui = uic.loadUi('./ui/word_analysis.ui')
        self.sql_helper = SqlHelper()
        self.label_picture = self.ui.label_picture
        self.pushButton_openNewTablePage = self.ui.pushButton_openNewTablePage
        self.init_picture()
        self.pushButton_openNewTablePage.clicked.connect(self.open_new_page)
    def open_new_page(self):
        SI.word_detailed_table_page = Word_detailed_table()
        SI.word_detailed_table_page.ui.show()
        # self.ui.hide()
    def init_picture(self):
        try:
            print('init')
            pixmap = QPixmap('picture/wordcloud.png')
            current_pixmap = self.label_picture.pixmap()
            # if current_pixmap:
            #     self.label_picture.clear()
            #     current_pixmap.detach()
            #     print('缓存以清除')
            self.label_picture.clear()
                # self.label_picture.setPixmap(None)
            self.label_picture.setPixmap(pixmap)
        except Exception as e:
            print(e)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Word_analysis()
    SI.page1.ui.show()
    app.exec()
