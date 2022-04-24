users = [
    {
        'id': 1,
        'username': 'felix',
        'password': 'abf8c407a0ac32aef0b62edd12177a73bab25600824267e05a39cb8306bce983'
    },
    {
        'id': 2,
        'username': 'flask',
        'password': 'abf8c407a0ac32aef0b62edd12177a73bab25600824267e05a39cb8306bce983'
    },
]


def get_user_by_username(username=None):
    for user in users:
        if user['username'] == username:
            return user


def insert_user(username, password):
    user = {
        'id': len(users) + 1,
        'username': username,
        'password': password
    }
    users.append(user)
    return user
