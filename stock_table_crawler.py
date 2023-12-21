import ssl
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QTableWidget
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lib.share import SI
from stock_chart import StockChartCrawler

ssl._create_default_https_context = ssl._create_unverified_context


class WorkThread(QThread):
    data_fetched_signal = pyqtSignal(list, list)

    def run(self):
        print('run')
        data_list, info_url_list = StockTableCrawler.crawl()
        print(info_url_list)
        # print(data_list)
        self.data_fetched_signal.emit(data_list, info_url_list)


class StockTableCrawler:
    def __init__(self):
        self.ui = uic.loadUi('./ui/stock_table.ui')
        icon = QIcon('image/logo.png')  # 替换为你的图标文件的路径
        self.ui.setWindowIcon(icon)
        self.ui.pushButton_update.clicked.connect(self.start_update)
        self.ui.pushButton_query.clicked.connect(self.query)
        self.ui.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.info_url_list = []

        self.worker_thread = None  # 初始化时不创建线程
        self.start_update()

    @staticmethod
    def crawl():
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://quote.eastmoney.com/stocklist.html')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        # print(soup)

        data_list = []
        info_url_list = []
        for tr in soup.find('tbody').find_all('tr'):
            td_data = []
            # 代码
            for idx, td in enumerate(tr.find_all('td')):
                if idx == 1:
                    info_url_list.append(td.find('a')['href'])
                # 过滤第四个和最后一个
                if idx not in (0, 3, len(tr.find_all('td')) - 1):
                    td_data.append(td.text.strip())
            data_list.append(td_data)
        return data_list, info_url_list

    def start_update(self):
        # if self.worker_thread is None or not self.worker_thread.isRunning():
        #     self.worker_thread = WorkThread()
        #     self.worker_thread.data_fetched_signal.connect(self.on_data_fetched)
        #     self.worker_thread.start()
        print('update')
        if self.worker_thread is None:
            print('init')
            self.worker_thread = WorkThread()
        if not self.worker_thread.isRunning():
            print('not running')
            # 添加 loading 显示
            self.ui.label_loading.setText('Loading...')
            self.worker_thread.data_fetched_signal.connect(self.on_data_fetched)
            self.worker_thread.start()

    def on_data_fetched(self, data_list, info_url_list):
        print('fetched')
        print(info_url_list)
        # 数据拉取
        self.ui.tableWidget.setRowCount(len(data_list))
        self.ui.tableWidget.setColumnCount(len(data_list[0]))
        # Insert data into the table
        for row_index, row_data in enumerate(data_list):
            for col_index, cell_value in enumerate(row_data):
                item = QTableWidgetItem(cell_value)
                self.ui.tableWidget.setItem(row_index, col_index, item)
        # 取消 loading 显示
        self.ui.label_loading.setText('')
        # 设置记录条数
        self.ui.label_record_count.setText(f'共 {len(data_list)} 条记录')
        # 更新表格
        self.ui.tableWidget.update()
        # 更新 url 列表
        self.info_url_list = info_url_list
        # QMessageBox.information(self.ui, '更新至最新', '已更新至最新', QMessageBox.Yes)
        # 断开之前的连接
        self.worker_thread.data_fetched_signal.disconnect(self.on_data_fetched)

    def query(self):
        print('查询图表')
        selected_items = self.ui.tableWidget.selectedItems()
        if selected_items:
            # 获取第一个选中项的行索引
            row_index = selected_items[0].row()
            print(f"Selected row index: {row_index}")
            # 操作
            SI.page3 = StockChartCrawler(self.info_url_list[row_index])
            SI.page3.ui.show()
        else:
            QMessageBox.information(self.ui, '警告', '未选中任何行', QMessageBox.Yes)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = StockTableCrawler()
    SI.page1.ui.show()
    sys.exit(app.exec_())
