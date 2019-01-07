import requests
import time
from bs4 import BeautifulSoup

PTT_URL = 'https://www.ptt.cc'


def getWebPage(url):
    # 取得網頁資料
    response = requests.get(url, cookies={'over18': '1'})
    if response.status_code == 200:
        return response.text
    else:
        print('無法抓取網頁:' + url)
        return None


def getArticles(htmldata, date):
    result = BeautifulSoup(htmldata, 'html.parser')
    # 尋找上頁連結
    pagingDiv = result.find('div', 'btn-group btn-group-paging')
    prevURL = pagingDiv.find_all('a')[1]['href']

    articles = []

    # 找出所有文章列表區塊
    divs = result.find_all('div', 'r-ent')
    for div in divs:
        # 處理個別文章內容
        # 非今天文章跳過不處理
        if div.find('div', 'date').text.strip() != date:
            continue
        # 處理推文數
        pushCount = 0
        pushString = div.find('div', 'nrec').text
        if pushString:
            try:
                pushCount = int(pushString)
            except ValueError:
                if pushString == '爆':
                    pushCount = 99
                elif pushString.startswith('X'):
                    pushCount = -10
        if div.find('a'):
            # 取得文章標題
            title = div.find('a').text
            # 取得文章超連結
            href = div.find('a')['href']
            # 取得作者
            author = div.find('div', 'author').text
            # 將處理過的文章資料放入 articles
            articles.append({'title': title,
                             'href': href,
                             'author': author,
                             'pushCount': pushCount})
    return articles, prevURL


# 主程式
print('處理:', PTT_URL + '/bbs/Gossiping/index.html')
htmldata = getWebPage(PTT_URL + '/bbs/Gossiping/index.html')
time.sleep(1)
# 取的今天日期
today = time.strftime('%m/%d').lstrip('0')
# 取得今天的文章
articles, prevURL = getArticles(htmldata, today)

todayArticles = []
while articles:
    todayArticles += articles
    print('處理', PTT_URL+prevURL)
    htmldata = getWebPage(PTT_URL + prevURL)
    articles, prevURL = getArticles(htmldata, today)
    time.sleep(1)

print(todayArticles)