from flask import render_template
from flask_login import login_required

from application import app


@app.route('/users')
@login_required
def users():
    return render_template('users.html')


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')
