from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, passhash):
        self.user_id = user_id
        self.username = username
        self.password = passhash

    @property
    def id(self):
        return self.username
