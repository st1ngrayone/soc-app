from datetime import datetime as dt

from werkzeug.utils import redirect
from flask_login import login_required, current_user
from flask import render_template, url_for, flash, request, jsonify

from application import app
from application.forms import PostForm
from application.entity.post import Post
from application.cache import Cache, CACHE_LIMIT
from application.dao import get_posts_by_follower
from application.dao import get_posts, get_posts_over_id
from application.dao import get_followers, get_post_by_id
from application.dao import add_new_follower, add_new_post


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
    cache = Cache('data_')
    free = cache.cache_free_space()

    if free == CACHE_LIMIT:
        # кэш пустой - берем все из базы
        all_posts_data = get_posts(free)
    elif free > 0:
        # дополняем из базы
        latest_post_id = cache.get_latest_post_id()
        posts_from_cache = tuple(cache.get_all())
        posts_from_db = get_posts_over_id(free, latest_post_id)
        all_posts_data = posts_from_db + posts_from_cache
    else:
        # все из кэша
        all_posts_data = tuple(cache.get_all())

    form = PostForm()

    posts_data = sorted(all_posts_data, key=check_type, reverse=True)

    return render_template("posts.html", posts=posts_data, form=form)


def check_type(data):
    return data.get('created_at')


@app.route('/posts', methods=['POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        cache = Cache('data_')

        title = form.title.data
        body = form.body.data

        post = Post(
            user_id(), current_user.name, current_user.lastname,
            title, body, dt.now(), account_id_fk=user_id()
        )

        cache.remove_latest()

        saved_post = add_new_post(post)
        cache.add(saved_post)
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
        post_id = data['post_id']
        like_type = data['type']

        add_new_follower(
            user_id(), follower_id, post_id, like_type, dt.now()
        )

        post = get_post_by_id(post_id)

        cache = Cache('data_')
        cache.replace(post)

        return jsonify(data)
