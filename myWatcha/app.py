from flask import Flask, render_template
import requests
from selenium import webdriver

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# if __name__ == '__main__':  
#    app.run('0.0.0.0',port=5000,debug=True)

   # 셀레니움 조작
options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
options.add_argument('--no-sandbox')
# 혹은 options.add_argument("--disable-gpu")

# 서버에 크롬드라이버 어떻게 넣어서 경로 지정하는지????
driver = webdriver.Chrome(executable_path='/root/project/Sparta_Project_DJ/myWatcha/chromedriver', chrome_options=options)

# 내 아이디로 왓챠 로그인해보기
driver.get('https://watcha.com/ko-KR')
driver.implicitly_wait(3)
driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/nav/ul/li[1]/button').click()
driver.find_element_by_name('email').send_keys('djnex310@gmail.com')
driver.find_element_by_name('password').send_keys('dj487905')
driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/section/div/div/div/section/div/div/form/button').click()

driver.quit()

# # 영화진흥원 API에서 제목 가져오기
# url_basic = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
# url_key = '6593947d539b25762ea24637a21e22b6'
# url_num = '100' # 가져올 제목의 수
# url = url_basic + '?key=' + url_key + '&itemPerPage=' + url_num

# response = requests.get(url)
# response_json = response.json()
# movies = response_json['movieListResult']['movieList']

# for movie in movies :
#     # 필요없는 정보 제외 필요
#     name_kr = movie['movieNm']
#     name_en = movie['movieNmEn']
#     print(name_kr, name_en)
