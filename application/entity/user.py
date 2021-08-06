from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, passhash, name, lastname):
        self.user_id = user_id
        self.username = username
        self.password = passhash
        self.name = name
        self.lastname = lastname

    @property
    def id(self):
        return self.username
