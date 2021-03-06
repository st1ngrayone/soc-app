import hashlib

from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_user, current_user

from application import app
from application.entity.user import User
from application.extensions import login_manager
from application.forms import LoginForm, RegisterForm
from application.dao import get_account, add_new_account


@login_manager.user_loader
def load_user(username):
    account = get_account(username)
    if account:
        return User(
            account['id'], account['username'],
            account['password'],  account['name'],
            account['lastname']
        )
    return None


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def post_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        passhash = hashlib.md5(password.encode('utf8')).hexdigest()
        user = load_user(username)
        if user and user.password == passhash:
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('index'))
        else:
            flash('Не удалось осуществить вход', 'warning')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/register', methods=['POST'])
def post_register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        passhash = hashlib.md5(password.encode('utf8')).hexdigest()

        account = get_account(username)

        if account:
            flash('Такой пользователь уже существует!', 'warning')
            form.username.errors.append('Такой пользователь уже существует!')
        else:
            profile = form.populate_profile()
            add_new_account(username, passhash, profile)
            return redirect(url_for('login'))
    return render_template('register.html', form=form)
