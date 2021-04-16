import MySQLdb.cursors

from application.extensions import mysql


def get_user(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
    return cursor.fetchone()


def add_new_user(username, password, email, name, lastname):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s)',
                   (username, password, email, name, lastname))
    mysql.connection.commit()


def get_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT name, lastname, city FROM accounts WHERE name is not NULL')
    return cursor.fetchall()


def get_friends(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    query = 'SELECT U.username, U.email FROM accounts U, friends F ' \
            'WHERE U.id = % s AND CASE WHEN F.friend_one = 4 ' \
            'THEN F.friend_two = U.id WHEN F.friend_two = 5 THEN F.friend_one= U.id END'

    cursor.execute(query, (user_id,))
    return cursor.fetchall()
