import sys
from collections import Counter
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
from pyqt5_plugins.examplebutton import QtWidgets
from qtpy import uic
from db.sql_helper import SqlHelper
from lib.share import SI
from word_cloud_generate import WordCloudGenerate
from matplotlib import rcParams

class Word_detailed_table():
    def __init__(self):
        self.ui = uic.loadUi('./ui/get_detailed_table.ui')
        self.label_table = self.ui.label_table
        self.paint_table()

    def paint_table(self):
        result = self.detailed_list(20)
        x_values = []
        y_values = []
        for item in result:
            x_values.append(item[0])
            y_values.append(item[1])

        # 创建一个 FigureCanvasQTAgg
        figure, ax = plt.subplots()
        ax.plot(x_values, y_values, label='热点线条')
        plt.xticks(rotation=45, ha="right")  # 适当旋转 x 轴标签
        ax.tick_params(axis='x', labelsize=8)
        ax.set_title('热点折线图')
        ax.set_xlabel('热点词')
        ax.set_ylabel('数量')
        ax.legend()

        # 保存图形到临时文件
        temp_file_path = 'picture/temp_plot.png'
        rcParams['font.sans-serif'] = ['SimSun']
        rcParams['font.size'] = 3
        figure.savefig(temp_file_path, bbox_inches='tight', pad_inches=0.1, dpi=300, format='png', transparent=True)
        plt.close(figure)

        # 将图形显示在 QLabel 中
        pixmap = QPixmap(temp_file_path)
        self.label_table.setPixmap(pixmap)
        self.label_table.setScaledContents(True)

    def detailed_list(self, i):
        db = SqlHelper()
        resultsina = db.get_list(
            'select * from sina_crawler_nationalNews UNION select * from sina_crawler_LocalNews UNION select * from sina_crawler_InternationalNews  ',
            [])
        resultzhenjuan = db.get_list(
            'select * from crawler_tb4  UNION select * from crawler_tb3  UNION select * from crawler_tb2   UNION select * from crawler_tb1  ;',
            [])
        res = resultsina + resultzhenjuan

        contents = ''
        for r in res:
            contents += r['content']
        wcg = WordCloudGenerate(contents, '../picture/test.png')
        result = wcg.getlist()
        result = [item for item in result if item.isalnum()]
        result = [item for item in result if not item.isdigit()]

        print(Counter(result).most_common(i))
        return Counter(result).most_common(i)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = Word_detailed_table()
    SI.page1.ui.show()
    app.exec()
