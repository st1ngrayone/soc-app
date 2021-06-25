from datetime import datetime as dt

from werkzeug.utils import redirect
from flask_login import login_required, current_user
from flask import render_template, url_for, flash, request, jsonify

from application import app
from application.dao import add_new_follower, add_new_post, get_posts
from application.dao import get_posts_by_follower, get_followers, get_followings
from application.forms import PostForm


def user_id():
    return current_user.user_id


@app.route('/posts')
@login_required
def posts():
    form = PostForm()
    posts_for_user = get_posts_by_follower(user_id())
    return render_template("posts.html", posts=posts_for_user, form=form)


@app.route('/posts/all')
@login_required
def all_posts():
    form = PostForm()
    all_posts_data = get_posts()
    return render_template("posts.html", posts=all_posts_data, form=form)


@app.route('/posts', methods=['POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        add_new_post(user_id(), title, body, dt.now())
        flash('Новый пост добавлен!', 'success')
        return redirect(url_for('all_posts'))
    else:
        flash('Произошла ошибка!', 'warning')
    return render_template('posts.html', form=form)


@app.route('/followers')
@login_required
def followers():
    followers_data = get_followers(user_id())
    return render_template('posts.html', followers=followers_data)


@app.route('/follow', methods=['POST'])
@login_required
def add_follower():
    data = request.get_json(force=True)

    if 'followerId' in data:
        follower_id = data['followerId']
        like_type = data['type']
        add_new_follower(user_id(), follower_id, like_type, dt.now())
        return jsonify(data)
