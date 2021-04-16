from flask import render_template
from flask_login import login_required, current_user

from application.dao import get_users, get_friends
from application import app


@app.route('/users')
@login_required
def users():
    users_data = get_users()
    return render_template('users.html', users=users_data)


@app.route('/friends')
@login_required
def friends():
    users_data = get_friends(current_user.user_id)
    return render_template('friends.html', users=users_data)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')
