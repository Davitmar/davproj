import hashlib
import sys


def hash_password(password):
    salt = bytes('(*&TYPuoy8&T(%8op9uIYGO*7', 'utf-8')

    dk = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt, 100000)

    return dk.hex()


if __name__ == '__main__':
    print(hash_password(sys.argv[1]))
