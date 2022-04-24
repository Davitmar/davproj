import hashlib
def hash_pass(password):
    h=hashlib.sha256(password.encode('utf-8')).hexdigest()
    return h

print(hash_pass(str('4555')))