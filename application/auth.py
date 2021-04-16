import re
from flask import render_template, request, redirect, url_for
from flask_login import logout_user, login_user, current_user

from application import app
from application.dao import get_user, add_new_user
from application.extensions import login_manager
from application.user import User


@login_manager.user_loader
def load_user(username):
    account = get_user(username)
    if account:
        return User(account['id'], account['username'], account['password'])
    return None


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    msg = ''
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = load_user(username)
        if user and user.password == password:
            login_user(user)
            next = request.args.get('next')
            msg = 'Logged in successfully!'
            return redirect(next or url_for('index', msg=msg))
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']

        account = get_user(username)

        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            add_new_user(username, password, email, name, lastname)
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)
