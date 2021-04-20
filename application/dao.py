import MySQLdb.cursors

from application.extensions import mysql


def get_account(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
    return cursor.fetchone()


def add_new_account(username, password, profile):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)',
        (
            username,
            password,
            profile.email,
            profile.name,
            profile.lastname,
            profile.city,
            profile.birth_date,
            profile.gender
        )
    )
    mysql.connection.commit()


def update_account(profile, user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    query = 'UPDATE accounts ' \
            'SET ' \
            'email =  %s, name = %s, lastname = %s, city = %s, birth_date = %s, gender = %s' \
            'WHERE id = % s'

    cursor.execute(query, (profile.email, profile.name, profile.lastname,
                           profile.city, profile.birth_date, profile.gender, user_id))
    mysql.connection.commit()


def get_accounts(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT a.id, a.name, a.lastname, a.city, f.status FROM accounts a '
        'left join friends f on a.id = f.friend_one'
        'WHERE a.name is not NULL AND a.id != %s'
        , (user_id,)
    )
    return cursor.fetchall()


def add_friend(user_id, other_user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO friends (friend_one, friend_two) VALUES (%s, %s)', (
            user_id, other_user_id
        )
    )
    mysql.connection.commit()


def confirm_friend(user_id, other_user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = 'UPDATE friends ' \
            'SET status="1" ' \
            'WHERE (friend_one=%s OR friend_two=%s) AND' \
            '(friend_one=%s OR friend_two=%s)'
    cursor.execute(query, (user_id, user_id, other_user_id, other_user_id))
    mysql.connection.commit()


def get_friends(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    query = 'select ac.name, ac.lastname from accounts a ' \
            'inner join friends f on a.id = f.friend_one ' \
            'inner join accounts ac on ac.id = f.friend_two ' \
            'where f.friend_one = % s'

    # query = 'SELECT U.username, U.email FROM accounts U, friends F ' \
    #        'WHERE U.id = % s AND CASE WHEN F.friend_one = 4 ' \
    #        'THEN F.friend_two = U.id WHEN F.friend_two = 5 THEN F.friend_one= U.id END'

    cursor.execute(query, (user_id,))
    return cursor.fetchall()
