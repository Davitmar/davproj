from hashlib import sha256

def coding(a=''):
    c=sha256(a.encode('utf-8')).hexdigest()
    return c
