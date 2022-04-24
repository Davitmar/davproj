from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import json
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
url = 'https://cwur.org/2021-22.php'
response = requests.get(url, headers=headers)
html_txt = response.text
soup = BeautifulSoup(html_txt, 'html.parser')
cont = soup.find(id='cwurTable').find_all('tr')

for i in cont[1:]:
    ham = Hamalsaran(rank=i.contents[0].text, name=i.contents[1].text, country=i.contents[2].text,
                     score=i.contents[-1].text)
    db.session.add(ham)
db.session.commit()




