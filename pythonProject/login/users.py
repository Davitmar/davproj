# users = [
#     {
#         'id': 1,
#         'username': 'felix',
#         'password': '123'
#     },
#     {
#         'id': 2,
#         'username': 'flask',
#         'password': '123'
#     },
# ]
#
#
# def get_user_by_username(username=None):
#     for user in users:
#         if user['username'] == username:
#             return user
#
# def add_new_user(username=None,password=None):
#     users.append({'id':len(users)+1, 'username':username,'password':password})
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/foo',methods=['GET', 'POST'])
def foo():
    return 'OK', 200
# import requests
# response = requests.post('http://127.0.0.1:5000/foo', {})
# print(response.status_code)

if __name__=='__main__':
    app.run()