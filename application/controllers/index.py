from flask_login import login_required
from flask import render_template, request, url_for
from werkzeug.utils import redirect

from application import app
from application.dao import search_users


@app.route('/search')
def search():
    results_data = []
    name = request.args.get('name')
    lastname = request.args.get('lastname')

    if name or lastname:
        results_data = search_users(name, lastname)

    return render_template(
        'search.html',
        results=results_data,
        name=name,
        lastname=lastname
    )


@app.route('/')
@app.route('/index')
@login_required
def index():
    return redirect(url_for('posts'))
