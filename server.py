#!/usr/bin/env python3

from flask import Flask
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from functools import wraps
from user import User

app = Flask(__name__)
ERR_BAD_LOGIN = "Bad username or password"
ERR_BAD_USERNAME = "Usernames must be 3 or more characters"
ERR_BAD_PASSWORD = "Passwords must be 8 or more characters"
ERR_USERNAME_TAKEN = "Username already taken"

COOKIE_TIMEOUT = 60 * 60 * 24 * 30  # 30 Days


def set_cookie(resp, user):
    resp.set_cookie("username", user.username, max_age=COOKIE_TIMEOUT)
    resp.set_cookie("token", user.new_cookie(), max_age=COOKIE_TIMEOUT)


def gen_session(resp, user):
    resp.set_cookie("username", user.username, max_age=COOKIE_TIMEOUT)
    resp.set_cookie("session", user.new_session())


def verify_cookie(func):
    @wraps(func)
    def f(*args, **kwargs):
        token = request.cookies.get("token", "")
        username = request.cookies.get("username", "")
        user = User.getByUsername(username)
        if user and user.verify_cookie(token):
            resp = make_response(func(*args, **kwargs))
            if user.needs_reset(token):
                user.invalidate_cookie(token)
                set_cookie(resp, user)
            gen_session(resp, user)
            return resp
        return redirect(url_for('login'))
    return f


def verify_session(func):
    @wraps(func)
    def f(*args, **kwargs):
        token = request.cookies.get("token", "")
        session = request.cookies.get("session", "")
        username = request.cookies.get("username", "")
        user = User.getByUsername(username)
        if user:
            resp = make_response(func(*args, **kwargs))
            if user.verify_session(session):
                user.extend_session(session)
            elif user.verify_cookie(token):
                gen_session(resp, user)
            return resp
        return redirect(url_for('login'))
    return f


@app.route('/', methods=['GET'])
@verify_cookie
def index():
    return redirect(url_for('todo'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    remember = request.form.get("remember", False)

    user = User.getByUsername(username)
    if user is None:
        return render_template('login.html', error=ERR_BAD_LOGIN)
    elif user.verify_password(password):
        resp = make_response(redirect(url_for('todo')))
        if remember:
            set_cookie(resp, user)
        return resp
    else:
        return render_template('login.html', error=ERR_BAD_LOGIN)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    remember = request.form.get("remember", False)
    if len(username) < 2:
        return render_template("register.html", error=ERR_BAD_USERNAME)
    if len(password) < 8:
        return render_template("register.html", error=ERR_BAD_PASSWORD)
    user = User.createUser(username, password)
    if not user:
        return render_template("register.html", error=ERR_USERNAME_TAKEN)
    resp = make_response(redirect(url_for('todo')))
    if remember:
        set_cookie(resp, user)
    return resp


@app.route('/todo', methods=['GET'])
@verify_session
def todo():
    if request.method == "GET":
        return render_template("todo.html")
    return "Nada yet"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
