import ssl
import time
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from db.sql_helper import SqlHelper

ssl._create_default_https_context = ssl._create_unverified_context


class Article:
    def __init__(self, title, time, tags, content):
        self.title = title
        self.time = time
        self.tags = tags


# 不显示浏览器
chrome_options = Options()
chrome_options.add_argument("--headless")

# url = 'https://company.cnstock.com/company/scp_gsxw/1'
# page = urllib.request.urlopen(url)
# soup = BeautifulSoup(page, 'html.parser')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://company.cnstock.com/company/scp_gsxw/1')
soup = BeautifulSoup(driver.page_source, 'html.parser')
# chrome_options.add_argument('--headless')

db = SqlHelper()

article_list = []
# 所有 li
li = soup.select(f'#j_waterfall_list > li')

# 加载到 100 条
while len(li) < 100:
    driver.execute_script("document.querySelector('#j_more_btn').click();")
    # wait = WebDriverWait(driver, 10)
    # new_page_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="new-page-content"]')))
    # wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="new-page-content"]')))
    # print(driver.page_source)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    li = soup.select(f'#j_waterfall_list > li')
    time.sleep(5)
    print(len(li))

for item in li:
    # 标签
    tags = []
    tag_selector = item.select('.info > .key')
    for i in range(len(tag_selector)):
        tags.append(tag_selector[i].contents[0])
    tags_str = ','.join(tags)
    content_url = item.select('h2 > a')[0]['href']
    url = 'https://company.cnstock.com/company/scp_gsxw/1'
    page = urllib.request.urlopen(content_url)
    soup = BeautifulSoup(page, 'html.parser')
    if not soup.select('.title'):
        continue
    # 标题
    title = soup.select('.title')[0].get_text()
    # 时间
    time = soup.select('.timer')[0].get_text()
    # 内容
    content = soup.select('#qmt_content_div')[0].get_text().strip()
    article_list.append((title, time, tags_str, content))
db.multiple_modify('insert into crawler_tb1 values(null, %s, %s, %s, %s)', article_list)
print('finish')
