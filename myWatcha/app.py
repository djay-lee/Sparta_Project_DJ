from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

# 영화진흥원 API에서 제목 가져오기
url_basic = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
url_key = '6593947d539b25762ea24637a21e22b6'
url_num = '100' # 가져올 제목의 수
url = url_basic + '?key=' + url_key + '&itemPerPage=' + url_num

response = requests.get(url)
response_json = response.json()
movies = response_json['movieListResult']['movieList']

for movie in movies :
    # 필요없는 정보 제외 필요
    name_kr = movie['movieNm']
    name_en = movie['movieNmEn']
    print(name_kr, name_en)
