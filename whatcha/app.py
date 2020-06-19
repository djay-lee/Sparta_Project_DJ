from flask import Flask, render_template, jsonify
import requests
# from selenium import webdriver
# import os
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# import time
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client.dbproject

# from pyvirtualdisplay import Display

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# if __name__ == '__main__':
#    app.run('0.0.0.0',port=5000,debug=True)

# display = Display(visible=0, size=(800, 800))
# display.start()


# 영화진흥원 API에서 제목 가져오기
def get_titles():
    url_basic = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    url_key = '6593947d539b25762ea24637a21e22b6'
    url_num = '10'  # 가져올 제목의 수
    url = url_basic + '?key=' + url_key + '&itemPerPage=' + url_num

    response = requests.get(url)
    response_json = response.json()
    movies = response_json['movieListResult']['movieList']

    titles = []
    for movie in movies:
        if '단편' not in movie['movieNm'] or 'cicaf' not in movie['movieNm'] or 'msff' not in movie['movieNm']:
            titles.append({'title_kr': movie['movieNm'],'title_en': movie['movieNmEn']}) 

# bs4로 url 모으기
# 주기적으로 전부 실행할 필요는 없고, 새로운 데이터들만 append하면 될 것 같음
# 새로운 영화 리스트를 어디서 받아오지? 매번 몇만개를 가져오긴 좀 그런데
def get_info():
    # 1. 영화진흥원 API에서 titles 가져오기
    url_basic = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    url_key = '6593947d539b25762ea24637a21e22b6'
    url_num = '1000'  # 가져올 제목의 수
    url = url_basic + '?key=' + url_key + '&itemPerPage=' + url_num

    response = requests.get(url)
    response_json = response.json()
    movies = response_json['movieListResult']['movieList']

    titles = []
    for movie in movies:
        if '단편' not in movie['movieNm'] or 'cicaf' not in movie['movieNm'] or 'msff' not in movie['movieNm']:
            titles.append({'title_kr': movie['movieNm'],'title_en': movie['movieNmEn']}) 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # titles = list(db.titles.find({}, {'_id': 0}))

    # 2. titles로 왓챠 검색해서 나오는 영화들 url 모으기
    url_list = []

    for title in titles:
        title_kr = title['title_kr']
        # title_en = title['title_en']
        data = requests.get(
            'https://watcha.com/ko-KR/searches/movies?query={}'.format(title_kr), headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        rows = soup.select(
            '# root > div > div.css-1sh3zvx-NavContainer.ebsyszu0 > section > section > div > div.css-1gkas1x-Grid.ejny11m0 > div > ul > li')
        for row in rows:
            url = row.select_one('a')
            if url is not None:
                url_list.append(url)

    # 3. 모인 url 하나씩 들어가서 영화정보 모으기
    for url in url_list:
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        poster = soup.select('root > div > div.css-1sh3zvx-NavContainer.ebsyszu0 > section > div > div > div > section > div.css-mrf2sf-PosterContainer.e1svyhwg1 > div.css-16l0ojz-MaxWidthGrid.e445inc0 > div > div > div > div > img')
        year = soup.select('root > div > div.css-1sh3zvx-NavContainer.ebsyszu0 > section > div > div > div > section > div.css-m4wuz0-PosterContainer.e1svyhwg1 > div.css-16l0ojz-MaxWidthGrid.e445inc0 > div > div > div > div > img')
        genre = soup.select()
        nation = soup.select()
        director = soup.select()
        actor = soup.select()
        plot = soup.select()
        star = soup.select()
        raters = soup.select()

        info = {'poster':poster,'year':year,'genre':genre,'nation':nation,'director':director,'actor':actor,'plot':plot,'star':star,'raters':raters}
        db.info.insert_one(info)

# 셀레니움으로 정보 모으기
# def get_info_slnm():
    # 셀레니움 조작
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("--disable-gpu")
    # options.add_argument('--no-sandbox')
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--remote-debugging-port=9222")
    # options.add_argument("--log-level=3")
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    # 크롬드라이버 실행, 왓챠 접속
    # driver = webdriver.Chrome(
    #     '/root/project/usr/bin/chromedriver', chrome_options=options)
    # driver.implicitly_wait(1)

    # titles = list(db.titles.find({}, {'_id': 0}))

    # for title in titles:
    #     title_kr = title['title_kr']
    #     title_en = title['title_en']
    #     driver.get(
    #         'https://watcha.com/ko-KR/searches/movies?query={}'.format(title_kr))
    # root > div > div.css-1sh3zvx-NavContainer.ebsyszu0 > section > section > div > div.css-1gkas1x-Grid.ejny11m0 > div > ul > li:nth-child(1) > a
    # root > div > div.css-1sh3zvx-NavContainer.ebsyszu0 > section > section > div > div.css-1gkas1x-Grid.ejny11m0 > div > ul > li:nth-child(2) > a
        # driver.get(
        #     'https://watcha.com/ko-KR/searches/movies?query={}'.format(title_en))

    # 왓챠 메인에서 영화 검색하기
    # driver.get('https://watcha.com/ko-KR')
    # driver.find_element_by_name('search').send_keys('바람과 함께~~')
    # driver.find_element_by_name("search").send_keys(Keys.ENTER)
    # driver.implicitly_wait(3)

    # driver.save_screenshot('jebal.png')

    # 내 아이디로 왓챠 로그인해보기 (실패)
    # driver.implicitly_wait(3)
    # driver.execute_script("window.scrollTo(0, 100)")
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/nav/ul/li[1]/button').click()
    # time.sleep(1)
    # driver.find_element_by_name('email').send_keys('djnex310@gmail.com')
    # driver.find_element_by_name('password').send_keys('dj487905')
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/section/div/div/div/section/div/div/form/button').click()
    # time.sleep(3)

    # driver.quit()
