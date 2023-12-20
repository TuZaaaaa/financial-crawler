import sys
import time
from PIL import Image

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
        print('init')
        pixmap = QPixmap('F:\\PytorchLearning\\financial-crawler\\picture\\wordcloud.png')
        self.label_picture.setPixmap(pixmap)
        self.label_picture.update()
        self.label_picture.repaint()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Word_analysis()
    SI.page1.ui.show()
    app.exec()
