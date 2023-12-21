import ssl
import threading
import time
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from db.sql_helper import SqlHelper

ssl._create_default_https_context = ssl._create_unverified_context


class StockCrawler:

    def __init__(self, urls=['https://company.cnstock.com/company/scp_gsxw/1', 'https://ggjd.cnstock.com/company/scp_ggjd/tjd_bbdj', 'https://ggjd.cnstock.com/company/scp_ggjd/tjd_ggkx', 'https://jrz.cnstock.com/'], load_num=20):
        self.urls = urls
        self.load_num = load_num

    @staticmethod
    def crawl(url, load_num, tb_num):
        try:
            # 不显示浏览器
            chrome_options = Options()
            chrome_options.add_argument("--headless")

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # 数据库
            db = SqlHelper()
            article_list = []
            # 所有 li
            li = soup.select(f'#j_waterfall_list > li')

            # 加载到 100 条
            while len(li) < load_num:
                driver.execute_script("document.querySelector('#j_more_btn').click();")
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                li = soup.select(f'#j_waterfall_list > li')
                time.sleep(5)
                print(len(li))

            driver.close()
            for item in li:
                # 标签
                tags = []
                tag_selector = item.select('.info > .key')
                for i in range(len(tag_selector)):
                    tags.append(tag_selector[i].contents[0])
                tags_str = ','.join(tags)
                content_url = item.select('h2 > a')[0]['href']
                page = urllib.request.urlopen(content_url)
                soup = BeautifulSoup(page, 'html.parser')
                if not soup.select('.title'):
                    continue
                # 标题
                title = soup.select('.title')[0].get_text()
                # 时间
                upload_time = soup.select('.timer')[0].get_text()
                # 内容
                content = soup.select('#qmt_content_div')[0].get_text().strip()
                article_list.append((title, upload_time, tags_str, content))
            db.modify(f'truncate table crawler_tb{tb_num}', [])
            db.multiple_modify(f'insert into crawler_tb{tb_num} values(null, %s, %s, %s, %s)', article_list)
            print('finish')
        except Exception as e:
            print(f"爬取失败 {url}: {e}")

    def run(self):
        threads = []
        # 加载的数量
        for i in range(len(self.urls)):
            thread = threading.Thread(target=self.crawl, args=(self.urls[i], self.load_num, i + 1))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        return 1
