import json
import requests

host = 'http://127.0.0.1:5000/'


def get_book(university_id):
    response = requests.get(f'{host}profile/{book_id}/')

    print('Status code:', response.status_code)
    print(response.json())


def get_universities():
    response = requests.get(f'{host}profile/')

    print('Status code:', response.status_code)
    print(response.json())


def add_user(payload):
    response = requests.post(f'{host}signup/', json.dumps(payload), headers={'Content-type': 'application/json'})

    print('Status code:', response.status_code)
    print(response.json())

token=None

def login(payload):
    response = requests.post(f'{host}login/', json.dumps(payload), headers={'Content-type': 'application/json'})

    print('Status code:', response.status_code)
    global token
    data = response.json()
    token=data['token']
    print(token)

def add_book(payload):
    global token
    response = requests.post(f'{host}addbook/', json.dumps(payload), headers={'Content-type': 'application/json', 'token':token})

    print('Status code:', response.status_code)
    print(response.json())


def update_university(university_id, payload):
    response = requests.put(f'{host}universities/{university_id}/', json.dumps(payload),
                            headers={'Content-type': 'application/json'})

    print('Status code:', response.status_code)
    print(response.json())


payload = {'username': 'Felix', 'password': 321}
login(payload)
payload = {'author': 'test_author2', 'name': 'test_name2'}
#print(token)
add_book(payload)

