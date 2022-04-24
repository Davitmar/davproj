import json

import requests


host = 'http://127.0.0.1:5000/'


def get_university(university_id):
    response = requests.get(f'{host}universities/{university_id}/')
    
    print('Status code:', response.status_code)
    print(response.json())


def get_universities():
    response = requests.get(f'{host}universities/')
    
    print('Status code:', response.status_code)
    print(response.json())


def create_university(payload):
    response = requests.post(f'{host}universities/', json.dumps(payload), headers={'Content-type': 'application/json'})
    
    print('Status code:', response.status_code)
    print(response.json())


def delete_university(university_id):
    response = requests.delete(f'{host}universities/{university_id}/')
    
    print('Status code:', response.status_code)
    print(response.json())


def update_university(university_id, payload):
    response = requests.put(f'{host}universities/{university_id}/', json.dumps(payload), headers={'Content-type': 'application/json'})
    
    print('Status code:', response.status_code)
    print(response.json())

payload={'rank':8504, 'name':'Huzhou Univer', 'country_id':3, 'score':369}

#get_universities()
#update_university(6, payload)
#get_university(2001)
delete_university(2001)
get_university(2001)
# id = db.Column(db.Integer, primary_key=True)
# rank = db.Column(db.Integer, nullable=False, unique=True)
# name = db.Column(db.String(250), nullable=False, unique=True)
# country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
# score = db.Column(db.Float(1), nullable=False)