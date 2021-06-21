import MySQLdb.cursors

from application.extensions import mysql


def get_account(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
    return cursor.fetchone()


def add_new_account(username, password, profile):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, NULL, %s, NULL, %s, %s)',
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
            'email =  %s, name = %s, lastname = %s, city = %s, birth_date = %s, gender = %s ' \
            'WHERE id = % s'

    cursor.execute(query, (profile.email, profile.name, profile.lastname,
                           profile.city, profile.birth_date, profile.gender, user_id))
    mysql.connection.commit()


def get_accounts(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT a.id, a.name, a.lastname, a.city FROM accounts a '
        'WHERE a.name is not NULL and a.id != %s and a.id not in '
        '(select distinct friend_two from friends where friend_one = %s) '
        , (user_id, user_id)
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
            'where f.friend_one = % s limit 30'

    # query = 'SELECT U.username, U.email FROM accounts U, friends F ' \
    #        'WHERE U.id = % s AND CASE WHEN F.friend_one = 4 ' \
    #        'THEN F.friend_two = U.id WHEN F.friend_two = 5 THEN F.friend_one= U.id END'

    cursor.execute(query, (user_id,))
    return cursor.fetchall()


def search_users(name, lastname):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = 'SELECT id, name, lastname from accounts ' \
            'where name like % s and lastname like % s ' \
            'order by id ' \
            'limit 1000 '

    cursor.execute(query, ((name + '%'), (lastname + '%')))
    return cursor.fetchall()


def add_new_post(user_id, body, created_at):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO posts VALUES (NULL, %s, %s, %s, NULL)',
        (
            user_id,
            body,
            created_at
        )
    )
    mysql.connection.commit()


def get_posts():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT p.*, ac.name, ac.lastname FROM posts p '
        'JOIN accounts ac on ac.id = p.account_id_fk '
        'ORDER BY p.created_at DESC limit 30 '
    )
    return cursor.fetchall()


def get_posts_by_follower(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT p.id, p.account_id_fk, p.body, f.target_id, ac.name, ac.lastname ' 
        'FROM posts p '
        'JOIN accounts ac on ac.id = p.account_id_fk '
        'LEFT JOIN followers f on f.target_id = p.account_id_fk '
        'WHERE f.source_id = %s', (user_id,)
    )
    return cursor.fetchall()


def add_new_follower(user_id, other_user_id, _type, created_at):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO followers VALUES (NULL, %s, %s, %s, %s, NULL)',
        (
            user_id,
            other_user_id,
            _type,
            created_at
        )
    )
    mysql.connection.commit()


def get_followers(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM followers WHERE target_id = %s', (user_id,)
    )
    return cursor.fetchall()


def get_followings(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM followers WHERE source_id = %s', (user_id,)
    )
    return cursor.fetchall()
