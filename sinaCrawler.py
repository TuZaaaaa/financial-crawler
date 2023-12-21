import urllib.request
from datetime import datetime

from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from db.sql_helper import SqlHelper

def returnHrefTitleBody(List,TagList=''):
    specificList = {}
    i = 0
    for title, href in List.items():
        url_new = href
        page_new = urllib.request.urlopen(url_new)
        soupNew = BeautifulSoup(page_new, 'html.parser')
        # print(soupNew)
        bodyNews = soupNew.find('div', {'class': 'article'})
        timeDiv = soupNew.find('div',{'class':'date-source'})
        time = timeDiv.find('span').get_text()
        # print(time)
        input_date = datetime.strptime(time, "%Y年%m月%d日 %H:%M")
        # 将datetime对象格式化为新的日期字符串
        output_date_str = input_date.strftime("%Y-%m-%d %H:%M:%S")
        bodyNewsList = bodyNews.find_all('p')
        resultNews = ''

        for bodyNewsItem in bodyNewsList:
            result = re.sub(r'<*[^>]*>(.*?)<\/*[^>]*>', r'\1', str(bodyNewsItem))
            # result = re.sub(r'\u3000', '', result)
            resultNews = resultNews + result
            # print(TagList)
            # print(i)
        specificList[href] = {'title': title, 'time': output_date_str, 'tag': TagList[i], 'body': resultNews}
        i += 1

    return specificList


def returnInternationalHrefTitleBody(List, TagList=''):
    specificList = {}
    # print(len(TagList))
    i = 0
    for title, href in List.items():
        url_new = href
        page_new = urllib.request.urlopen(url_new)
        soupNew = BeautifulSoup(page_new, 'html.parser')
        # print(soupNew)
        bodyNews = soupNew.find('div', {'class': 'article'})
        # print(soupNew)
        timeDiv = soupNew.find('div', {'class': 'date-source'})
        # print(timeDiv)
        if timeDiv!=None:
            time = timeDiv.find('span').get_text()
        else:
            time='1111年11月11日 11:11'

        # print(time)
        input_date = datetime.strptime(time, "%Y年%m月%d日 %H:%M")
        # 将datetime对象格式化为新的日期字符串
        output_date_str = input_date.strftime("%Y-%m-%d %H:%M:%S")
        bodyNewsList = bodyNews.find_all('p')
        resultNews = ''

        for bodyNewsItem in bodyNewsList:
            result = re.sub(r'<*[^>]*>(.*?)<\/*[^>]*>', r'\1', str(bodyNewsItem))
            # result = re.sub(r'\u3000', '', result)
            resultNews = resultNews + result
        # print(TagList)
            # print(i)

        specificList[href] = {'title': title, 'time': output_date_str, 'tag': TagList[i], 'body': resultNews}
        # print(specificList)
        i += 1
        # print(i)
        if i>= len(TagList):
            break
    return specificList

def returnLoaclHrefTitleBody(List,TagList=''):
    specificList = {}
    i = 0
    for title, href in List.items():
        url_new = href
        page_new = urllib.request.urlopen(url_new)
        soupNew = BeautifulSoup(page_new, 'html.parser')
        # print(soupNew)
        bodyNews = soupNew.find('div', {'class': 'article-body main-body'})
        timeDiv = soupNew.find('p',{'class':'source-time'})
        time = timeDiv.find('span').get_text()
        # print(time)
        input_date = datetime.strptime(time, "%Y-%m-%d %H:%M")
        # 将datetime对象格式化为新的日期字符串
        output_date_str = input_date.strftime("%Y-%m-%d %H:%M:%S")
        # print(bodyNews)
        bodyNewsList = bodyNews.find_all('p')
        resultNews = ''

        for bodyNewsItem in bodyNewsList:
            result = re.sub(r'<*[^>]*>(.*?)<\/*[^>]*>', r'\1', str(bodyNewsItem))
            # result = re.sub(r'\u3000', '', result)
            resultNews = resultNews + result
        # print(TagList)
        # print(i)
        if TagList=='':
            specificList[href] = {'title': title, 'time':output_date_str,'tag':'','body': resultNews}
        # print(specificList)
    return specificList

def useNoheadConnect(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    # chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(1)
    page_content = browser.page_source
    browser.quit()
    return page_content

# print(economicDiv)
# internationalEconomicNews={}
# internationalEconomicDiv = economicDiv.find('div',attrs={'class':'m-p3-l-blk1'})
# internationalEconomicUl = internationalEconomicDiv.find('ul')
# internationalEconomicList = internationalEconomicUl.find_all('a')
# # print(internationalEconomicList)
# for internationalEconomicItem in internationalEconomicList:
#     # print(internationalEconomicItem.get_text())
#     internationalEconomicNews[internationalEconomicItem.get_text()]=internationalEconomicItem['href']
# # print(internationalEconomicNews)
# internationalEconomicNewsSpecific={}
# for title,href in internationalEconomicNews.items():
#     # print(title,href)
#     # print(href)
#     url_new = href
#     page_new = urllib.request.urlopen(url_new)
#     soupNew = BeautifulSoup(page_new,'html.parser')
#     # print(soupNew)
#     bodyNews = soupNew.find('div',{'class':'article'})
#     bodyNewsList = bodyNews.find_all('p')
#     # print(bodyNewsList)
#     resultNews=''
#     for bodyNewsItem in bodyNewsList:
#         # print(bodyNewsItem)
#         result = re.sub(r'<*[^>]*>(.*?)<\/*[^>]*>', r'\1', str(bodyNewsItem))
#         result = re.sub(r'\u3000', '', result)
#         resultNews = resultNews+result
#     internationalEconomicNewsSpecific[href] = {'title':title,'body':resultNews}
# print(internationalEconomicNewsSpecific)

def getInternationalNews():
    # 获取国外新闻
    url = 'https://finance.sina.com.cn/'
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    economicDiv = soup.find('div',attrs={'class':'m-part m-part3 udv-clearfix'})
    moreEconomicNews = economicDiv.find('div',{'class':'part right fright'})
    # print(moreEconomicNews)
    moreEconomicNewshref=moreEconomicNews.find('a')['href']
    # print(moreEconomicNewshref)
    page = urllib.request.urlopen(moreEconomicNewshref)
    # print(page)
    soup = BeautifulSoup(page,'html.parser')
    # print(soup)
    # 找到包含重定向信息的 meta 标签
    meta_refresh_tag = soup.find('meta', {'http-equiv': 'refresh'})
    redirect_url=''
    if meta_refresh_tag:
        # 获取 content 属性中的重定向 URL
        content = meta_refresh_tag.get('content', '')
        redirect_url = content.split('URL=')[1] if 'URL=' in content else ''
    # print(redirect_url)
    # 设置 Chrome 无头模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    # chrome_options.add_argument('--disable-software-rasterizer') #GPU加速

    # 创建 Chrome 浏览器对象
    browser = webdriver.Chrome(options=chrome_options)

    # 打开网页
    browser.get(redirect_url)

    # 等待一定时间，确保页面加载完成（可以根据实际情况调整）
    browser.implicitly_wait(1)

    # 获取页面内容
    page_content = browser.page_source

    # 关闭浏览器
    browser.quit()

    # print(type(page_content))
    soup = BeautifulSoup(page_content,'html.parser')
    moreEconomicNewsDiv=soup.find('div',{'class':'cardlist-a__list'})
    # print(moreEconomicNewsDiv)
    moreEconomicNewsList={}
    moreEconomicNewsH3 = moreEconomicNewsDiv.find_all('h3',{'class':'ty-card-tt'})
    moreEconomicNewsTagSpan = moreEconomicNewsDiv.find_all('span',{'class':'ty-card-tip2-i ty-card-tags'})
    moreEconomicNewsTags=[]
    for moreEconomicNewsTagItem in moreEconomicNewsTagSpan:
        # print(moreEconomicNewsTagItem.find_all('a'))
        moreEconomicNewsTag=[]
        for moreEconomicNewsTagItem2 in moreEconomicNewsTagItem.find_all('a'):
            # print(moreEconomicNewsTagItem2)
            moreEconomicNewsTag.append(moreEconomicNewsTagItem2.get_text())
        moreEconomicNewsTags.append(moreEconomicNewsTag)
    # print(moreEconomicNewsTags)

    for moreEconomicNewsItem in moreEconomicNewsH3:
        # print(moreEconomicNewsItem.find('a')['href'])
        moreEconomicNewsList[moreEconomicNewsItem.find('a').get_text()]=moreEconomicNewsItem.find('a')['href']
    # print(moreEconomicNewsList)

    moreEconomicNewsSpecific = returnInternationalHrefTitleBody(moreEconomicNewsList,TagList=moreEconomicNewsTags)
    # print(moreEconomicNewsSpecific)
    db = SqlHelper()
    db.modify(f'truncate table sina_crawler_InternationalNews', [])
    article_list=[]
    for href,item in moreEconomicNewsSpecific.items():
        # print(href,item)
        ags_str = ','.join(item['tag'])
        article_list.append((item['title'],item['time'],ags_str,item['body']))
        # print(article_list)
    db.multiple_modify(f'insert into sina_crawler_InternationalNews values(null, %s, %s, %s, %s)', article_list)
    print('国际新闻爬取完成')
    return 1

def getNationalNews():
    # 获取国内新闻
    nationalNewsList = {}
    page_content = useNoheadConnect('https://finance.sina.com.cn/')
    soup = BeautifulSoup(page_content,'html.parser')
    # print(soup)
    nationalNewsDiv=soup.find_all('div',{'class','udv-clearfix m-more-tab'})[1]
    # print(nationalNewsDiv)
    # print(nationalNewsDiv.find_all('a'))

    nationalNewsHref = nationalNewsDiv.find_all('a')[0]['href']
    # print(nationalNewsHref)
    # page_content = useNoheadConnect(nationalNewsHref)


    url = nationalNewsHref
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式
    # 创建 Chrome 浏览器对象
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    TagList=[]
    while len(nationalNewsList)<10:
        print(len(nationalNewsList))
        page_content = browser.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        # print(soup)
        nationalNewsDiv2 = soup.find('div', {'class': 'feed-card-content'})
        nationalNewsTagDiv = nationalNewsDiv2.find_all('div',{'class':'feed-card-tags'})
        # print(nationalNewsTagDiv)
        for nationalNewsTagItem in nationalNewsTagDiv:
            # print(nationalNewsTagItem)
            nationalNewsTags = nationalNewsTagItem.find_all('a')
            nationalNewsTagsList = []
            for nationalNewsTagsItem in nationalNewsTags:
                # print(nationalNewsTagsItem.get_text())
                nationalNewsTagsList.append(nationalNewsTagsItem.get_text())
            TagList.append(nationalNewsTagsList)
        nationalNewsDivH2 = nationalNewsDiv2.find_all('h2')
        # print(nationalNewsDivH2)
        for nationalNewsItem in nationalNewsDivH2:
            # print(nationalNewsItem.find('div',{'class':'feed-card-tags'}))
            nationalNewsList[nationalNewsItem.find('a').get_text()] = nationalNewsItem.find('a')['href']

        browser.execute_script("document.querySelector('.pagebox_next a').click();")
        time.sleep(1)
    # print(len(TagList))
    # 关闭浏览器
    browser.quit()
    # print(returnHrefTitleBody(nationalNewsList,TagList))
    db = SqlHelper()
    # print(returnHrefTitleBody(nationalNewsList,TagList=TagList))
    db.modify(f'truncate table sina_crawler_nationalNews', [])
    article_list=[]
    for href,item in returnHrefTitleBody(nationalNewsList,TagList=TagList).items():
        ags_str = ','.join(item['tag'])
        article_list.append((item['title'],item['time'],ags_str,item['body']))
        # print(article_list)
    db.multiple_modify(f'insert into sina_crawler_nationalNews values(null, %s, %s, %s, %s)', article_list)
    print('国内新闻爬取完成')
    return 1

def getLocalNews():
    # 当地新闻
    nationalNewsList = {}
    page_content = useNoheadConnect('https://finance.sina.com.cn/')
    soup = BeautifulSoup(page_content, 'html.parser')
    # print(soup)
    nationalNewsDiv = soup.find_all('div', {'class', 'udv-clearfix m-more-tab'})[1]
    # print(nationalNewsDiv.find_all('a'))
    localNewsHref = nationalNewsDiv.find_all('a')[2]['href']
    # print(localNewsHref)
    url = localNewsHref
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式
    # 创建 Chrome 浏览器对象
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    page_content = browser.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    # print(soup)
    # print(soup.find('ul',{'class':'news-list cur'}))
    localNewsH2 = soup.find('ul', {'class': 'news-list cur'}).find_all('h2')
    localNewsList = {}
    for localNewsItem in localNewsH2:
        # print(localNewsItem.find('a'))
        localNewsList[localNewsItem.find('a').get_text()] = localNewsItem.find('a')['href']
    # print(localNewsList)
    # print(returnLoaclHrefTitleBody(localNewsList))
    db = SqlHelper()

    db.modify(f'truncate table sina_crawler_LocalNews', [])
    article_list=[]
    for href,item in returnLoaclHrefTitleBody(localNewsList).items():
        ags_str = ','.join(item['tag'])
        article_list.append((item['title'],item['time'],ags_str,item['body']))
        # print(article_list)
    db.multiple_modify(f'insert into sina_crawler_LocalNews values(null, %s, %s, %s, %s)', article_list)
    print('本地新闻爬取完成')
    return 1

def run():
    # getInternationalNews()
    # getNationalNews()
    getLocalNews()
    return 1


if __name__ == '__main__':
    getInternationalNews()
    getNationalNews()
    getLocalNews()
