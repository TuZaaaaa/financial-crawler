import ssl
import sys
import time

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lib.share import SI

ssl._create_default_https_context = ssl._create_unverified_context


class WorkThread(QThread):
    data_fetched_signal = pyqtSignal(list)

    def run(self):
        while True:
            data_list = StockTableCrawler.crawl()
            print(data_list)
            self.data_fetched_signal.emit(data_list)
            time.sleep(5)


class StockTableCrawler:
    def __init__(self):
        self.ui = uic.loadUi('./ui/stock_table.ui')

        self.worker_thread = None  # 初始化时不创建线程
        self.start_update()

    @staticmethod
    def crawl():
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://quote.eastmoney.com/stocklist.html')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup)

        data_list = []
        for tr in soup.find('tbody').find_all('tr'):
            td_data = []
            # 代码
            for idx, td in enumerate(tr.find_all('td')):
                # 过滤第四个和最后一个
                if idx not in (0, 3, len(tr.find_all('td')) - 1):
                    td_data.append(td.text.strip())
            data_list.append(td_data)
        return data_list

    def start_update(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.worker_thread = WorkThread()
            self.worker_thread.data_fetched_signal.connect(self.on_data_fetched)
            self.worker_thread.start()

    def on_data_fetched(self, data_list):
        # 数据拉取
        self.ui.tableWidget.setRowCount(len(data_list))
        self.ui.tableWidget.setColumnCount(len(data_list[0]))
        # Insert data into the table
        for row_index, row_data in enumerate(data_list):
            for col_index, cell_value in enumerate(row_data):
                item = QTableWidgetItem(cell_value)
                self.ui.tableWidget.setItem(row_index, col_index, item)
        # 设置记录条数
        self.ui.label_record_count.setText(f'共 {len(data_list)} 条记录')
        self.ui.tableWidget.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SI.page1 = StockTableCrawler()
    SI.page1.ui.show()
    sys.exit(app.exec_())
