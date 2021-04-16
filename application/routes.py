from flask import render_template
from flask_login import login_required

import MySQLdb.cursors
from application.extensions import mysql, login_manager

from application import app


@app.route('/users')
@login_required
def users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT name, lastname, city FROM accounts WHERE name is not NULL')
    users = cursor.fetchall()
    return render_template('users.html',users=users)

@app.route('/friends')
@login_required
def users():
    userid = cursor.fetchone()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT U.username, U.email FROM accounts U, friends F WHERE CASE WHEN F.friend_one = 4 THEN F.friend_two = U.id WHEN F.friend_two = 5 THEN F.friend_one= U.id END'), (userid, )
    users = cursor.fetchall()
    return render_template('users.html',users=users)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')
