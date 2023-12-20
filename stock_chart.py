import base64
import io
import ssl
import sys
import threading

from PIL import Image
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QMessageBox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ssl._create_default_https_context = ssl._create_unverified_context


class WorkThread(QThread):
    def __init__(self, chart_url):
        super().__init__()
        self.chart_url = chart_url

    data_fetched_signal = pyqtSignal()

    def run(self):
        print('run')
        StockChartCrawler.crawl(self.chart_url)
        self.data_fetched_signal.emit()


class StockChartCrawler:

    def __init__(self, chart_url):
        self.ui = uic.loadUi('./ui/stock_chart.ui')
        icon = QIcon('image/logo.png')  # 替换为你的图标文件的路径
        self.ui.setWindowIcon(icon)
        self.chart_url = chart_url

        # # 更新图片显示
        # lbl = QLabel(self.ui)
        # pixmap = QPixmap('img.png')
        # lbl.setPixmap(pixmap)  # 在label上显示图片
        # lbl.setScaledContents(True)  # 让图片自适应label大小
        # self.ui.verticalLayout.addWidget(lbl)

        self.worker_thread = None  # 初始化时不创建线程
        self.start_update()


    @staticmethod
    def crawl(chart_url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https:' + chart_url)
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # tab = soup.select('.mqc_tab2 a')[0]
        # 点击切换至 图片版
        driver.execute_script("document.querySelector('.mqc_tab2 a').click();")
        # 获取新的页面
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 获取图片 url
        img = soup.select('.time_static_img img')[0]
        img_src = img['src']
        print(img_src)

        # driver.get('https://webquotepic.eastmoney.com/GetPic.aspx?imageType=r&type=&token=44c9d251add88e27b65ed86506f6e5da&nid=0.833284&timespan=1702982769')
        driver.get('http:' + img_src)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(soup)
        driver.execute_script("var img = document.querySelector('img');var canvas = document.createElement('canvas'); var ctx = canvas.getContext('2d'); canvas.width = img.width;; canvas.height = img.height; ctx.drawImage(img, 0, 0); var dataURL = canvas.toDataURL('image/png'); console.log(dataURL); const paragraph = document.createElement('p'); const text = document.createTextNode(dataURL); paragraph.appendChild(text); document.body.appendChild(paragraph);")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        img_data = soup.find('p').text
        print(img_data)

        image_data = base64.b64decode(img_data[22:])
        image = Image.open(io.BytesIO(image_data))
        image.save("img.png")

    def start_update(self):
        if self.worker_thread is None:
            self.worker_thread = WorkThread(self.chart_url)
        if not self.worker_thread.isRunning():
            # 添加 loading 显示
            self.ui.label_loading.setText('Loading...')
            self.worker_thread.data_fetched_signal.connect(self.on_data_fetched)
            self.worker_thread.start()

    def on_data_fetched(self):
        print('aa')
        print('chart fetched')
        # 更新图片显示
        lbl = QLabel(self.ui)
        pixmap = QPixmap('img.png')
        lbl.setPixmap(pixmap)  # 在label上显示图片
        lbl.setScaledContents(True)  # 让图片自适应label大小
        self.ui.verticalLayout.addWidget(lbl)

        # 取消 loading 显示
        self.ui.label_loading.setText('')
        QMessageBox.information(self.ui, '更新至最新', '已更新至最新', QMessageBox.Yes)
        # 断开之前的连接
        self.worker_thread.data_fetched_signal.disconnect(self.on_data_fetched)
