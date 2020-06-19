from flask import Flask, render_template, jsonify
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client.dbproject

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# if __name__ == '__main__':
#    app.run('0.0.0.0',port=5000,debug=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get(
    'https://www.pgatour.com/players.html', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

players = soup.select('li.player-card')

urls = []

for player in players :
    # firstname = player.select_one('.player-firstname').text
    # surname = player.select_one('.player-surname').text
    # name = firstname + " " + surname
    # face = player.select_one('.player-image')['src']
    # nation = player.select_one('.player-country').text
    # 여기까진 기본페이지에 쫙 표시하기? 굳이?
    url = player.select_one('.player-link')['href']
    urls.append(url)
    # print(urls)
    # 모든 선수들의 프로필이 자세히 나와있는건 아니라서 유령들은 걸러야함

for url in urls :
    data = requests.get('https://www.pgatour.com'+url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    face = soup.select_one('div.s-header > div.s-photo > img.s-photo__item')['src']
    # face = profile.select_one('.s-photo__item')['src']
    if face is not None :
        print(face)