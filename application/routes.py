from flask import render_template
from flask_login import login_required

import MySQLdb.cursors
from application.extensions import mysql, login_manager

from application import app


@app.route('/users')
@login_required
def users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    users = cursor.execute('SELECT * FROM accounts')
    account = cursor.fetchone()
    return render_template('users.html',users=users)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')
