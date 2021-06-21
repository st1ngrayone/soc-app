from datetime import datetime

from werkzeug.utils import redirect
from flask_login import login_required, current_user
from flask import render_template, url_for, flash, request

from application import app
from application.dao import add_new_follower, add_new_post, get_posts
from application.dao import get_posts_by_follower, get_followers, get_followings


@app.route('/posts')
@login_required
def posts():
    posts_for_user = get_posts_by_follower(current_user.user_id)
    return render_template("posts.html", posts=posts_for_user)


@app.route('/posts/all')
@login_required
def all_posts():
    all_posts_data = get_posts()
    return render_template("posts.html", posts=all_posts_data)


@app.route('/posts', methods=['POST'])
@login_required
def new_post():
    if 'body' in request.form:
        body = request.form['body']
        add_new_post(current_user.user_id, body, datetime.now())
        flash('Новый пост добавлен!', 'success')
        return redirect(url_for('posts'))
    else:
        flash('Произошла ошибка!', 'warning')
    return render_template('posts.html')


@app.route('/followers')
@login_required
def followers():
    followers_data = get_followers(current_user.user_id)
    return render_template('posts.html', followers=followers_data)


@app.route('/follow', methods=['POST'])
@login_required
def add_follower():
    if 'followerId' in request.form:
        follower_id = request.form['followerId']
        _type = request.form['type']
        add_new_follower(
            current_user.user_id, follower_id, _type, datetime.now()
        )
    return redirect(url_for('followers'))
