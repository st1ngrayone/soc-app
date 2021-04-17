from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    @property
    def id(self):
        return self.username
