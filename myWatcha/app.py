import requests

url_basic = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
url_key = '6593947d539b25762ea24637a21e22b6'
url_num = '100'
url = url_basic + '?key=' + url_key + '&itemPerPage=' + url_num

response = requests.get(url)
response_json = response.json()
movies = response_json['movieListResult']['movieList']

for movie in movies :
    movie_korname = movie['movieNm']
    movie_engname = movie['movieNmEn']
    print(movie_korname, movie_engname)
