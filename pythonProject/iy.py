import jwt
import hashlib

def hash_pass(password):
    h=hashlib.sha256(password.encode('utf-8')).hexdigest()
    return h

key='jdjdvlkdklx'
password=123

token = jwt.encode({'id': 456, 'username': 'davit', 'password': hash_pass(str(password))}, key,
                       algorithm="HS256")
print(token)
decoded_token=jwt.decode(token, key, algorithms=["HS256"])
print(decoded_token)