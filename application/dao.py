import MySQLdb.cursors

from application.entity.post import Post
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
        '(select distinct friend_two from friends where friend_one = %s) limit 50 '
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
    query = 'SELECT name, lastname, city from accounts ' \
            'where name like % s and lastname like % s ' \
            'order by id ' \
            'limit 1000 '

    cursor.execute(query, ((name + '%'), (lastname + '%')))
    return cursor.fetchall()


def add_new_post(post: Post):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO posts VALUES (NULL, %s, %s, %s, %s, NULL)',
        (
            post.user_id,
            post.title,
            post.body,
            post.created_at
        )
    )
    mysql.connection.commit()

    post.id = cursor.lastrowid
    return post


def get_posts(limit):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT p.*, ac.name, ac.lastname,  '
        'SUM(CASE WHEN ff.type = "0" THEN 1 ELSE 0 END) as likes, '
        'SUM(CASE WHEN ff.type = "1" THEN 1 ELSE 0 END) as dislikes, '
        'SUM(CASE WHEN ff.type = "2" THEN 1 ELSE 0 END) as followers_count '
        'FROM posts p '
        'JOIN accounts ac on ac.id = p.account_id_fk '
        'LEFT JOIN followers ff on ff.post_id = p.id '
        'GROUP BY ff.source_id, p.id, p.account_id_fk, p.title, p.body, p.created_at '
        'ORDER BY p.created_at DESC limit %s', (limit,)
    )
    return cursor.fetchall()


def get_post_by_id(post_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT p.*, ac.name, ac.lastname,  '
        'SUM(CASE WHEN ff.type = "0" THEN 1 ELSE 0 END) as likes, '
        'SUM(CASE WHEN ff.type = "1" THEN 1 ELSE 0 END) as dislikes, '
        'SUM(CASE WHEN ff.type = "2" THEN 1 ELSE 0 END) as followers_count '
        'FROM posts p '
        'JOIN accounts ac on ac.id = p.account_id_fk '
        'LEFT JOIN followers ff on ff.post_id = p.id '
        'WHERE p.id = %s '
        'GROUP BY ff.source_id, p.id, p.account_id_fk, p.title, p.body, p.created_at ', (post_id,)
    )

    post_db = cursor.fetchone()

    post_db.pop('updated_at')

    return Post(
            user_id=post_db.get('account_id_fk'), **post_db
        )


def get_posts_over_id(limit, post_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT p.*, ac.name, ac.lastname, '
        'SUM(CASE WHEN ff.type = "0" THEN 1 ELSE 0 END) as likes, '
        'SUM(CASE WHEN ff.type = "1" THEN 1 ELSE 0 END) as dislikes, '
        'SUM(CASE WHEN ff.type = "2" THEN 1 ELSE 0 END) as followers_count '
        'FROM posts p '
        'JOIN accounts ac on ac.id = p.account_id_fk '
        'LEFT JOIN followers ff on ff.post_id = p.id '
        'WHERE p.id > %s '
        'GROUP BY ff.source_id, p.id, p.account_id_fk, p.title, p.body, p.created_at '
        'ORDER BY p.created_at DESC limit %s', (post_id, limit)
    )
    return cursor.fetchall()


def get_posts_by_follower(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT p.*, ac.name, ac.lastname,  '
        'SUM(CASE WHEN ff.type = "0" THEN 1 ELSE 0 END) as likes, '
        'SUM(CASE WHEN ff.type = "1" THEN 1 ELSE 0 END) as dislikes, '
        'SUM(CASE WHEN ff.type = "2" THEN 1 ELSE 0 END) as followers_count '
        'FROM posts p '
        'JOIN accounts ac on ac.id = p.account_id_fk '
        'LEFT JOIN followers ff on ff.post_id = p.id '
        'WHERE ff.source_id = %s and ff.type in ("0", "2")'
        'GROUP BY ff.source_id, p.id, p.account_id_fk, p.title, p.body, p.created_at '
        'ORDER BY p.created_at DESC limit 30', (user_id,)
    )
    return cursor.fetchall()


def add_new_follower(user_id, other_user_id, post_id, _type, created_at):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'INSERT INTO followers VALUES (NULL, %s, %s, %s, %s, %s, NULL) '
        'ON DUPLICATE KEY UPDATE type=VALUES(type)',
        (
            user_id,
            other_user_id,
            post_id,
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
