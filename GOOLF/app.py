from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('49.50.172.211', 27017)
db = client.dbproject

app = Flask(__name__)


# PGA 선수들 데이터 db에 저장
def player_data() :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = request.get(
        'https://www.pgatour.com/players.html', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # 선수별 url 모으기
    players = soup.select('li.player-card')
    urls = []
    for player in players :
        url = player.select_one('.player-link')['href']
        urls.append(url)

    # 선수별 data 크롤링하기
    for url in urls :
        data = request.get('https://www.pgatour.com'+url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        is_ghost = soup.select_one('.s-person__name')
        if is_ghost is not None : 
            is_ghost = is_ghost.text
            if is_ghost is not "" :
                infos = soup.select('.s-col__row')
                player_info = {}
                player_info['face'] = soup.select_one('.s-photo__item')['src']
                player_info['flag'] = soup.select_one('.s-flag')['src']
                player_info['nation'] = soup.select_one('.s-person__country').text
                for num in range(7) :
                    selector = infos[num].text
                    if 'Full Name' in selector :
                        player_info['name'] = infos[num].select_one('.s-top-text').text
                    if 'Height' in selector :
                        player_info['height'] = infos[num].select_one('.s-top-text.js-show-on-metric').text.strip('cm')
                    if 'Weight' in selector :
                        player_info['weight'] = infos[num].select_one('.s-top-text.js-show-on-metric').text.strip('kg')
                    if 'AGE' in selector :
                        player_info['age'] = infos[num].select_one('.s-top-text').text
                db.player_info.insert_one(player_info)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def user_give ():
    user_info = {}
    user_info['name'] = 'user'
    user_info['age'] = request.form['age_give']
    user_info['weight'] = request.form['weight_give']
    user_info['height'] = request.form['height_give']
    
    db.player_info.insert_one(user_info)

    return render_template("result.html")

@app.route('/get', methods=['GET'])
def player_give () :
    players = list(db.player_info.find({},{'_id':False}))
    
    return jsonify({'result': 'success','players_list':players})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)


