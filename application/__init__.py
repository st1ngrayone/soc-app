from flask import Flask

from config import Config
from application.extensions import login_manager, mysql

app = Flask(__name__)


def create_app(config_class=Config):
    app.config.from_object(config_class)

    from application import auth, controllers

    mysql.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = None
    return app
