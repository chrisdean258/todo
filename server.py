#!/usr/bin/env python3

from flask import Flask
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from user import User

app = Flask(__name__)
ERR_BAD_LOGIN = "Bad username or password"
ERR_BAD_USERNAME = "Usernames must be 3 or more characters"
ERR_BAD_PASSWORD = "Passwords must be 8 or more characters"
ERR_USERNAME_TAKEN = "Username already taken"

COOKIE_TIMEOUT=60*60*24*30 # 30 Days


@app.route('/', methods=['GET'])
def index(error=None):
    login_token = request.cookies.get("login_token", "")
    username = request.cookies.get("username", "")
    user = User.getByUsername(username)
    if user and user.verify_cookie(login_token):
        resp = make_response(redirect(url_for('todo')))
        resp.set_cookie("login_token", user.new_cookie())
        return resp
    return render_template("index.html", error=error)


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    remember = request.form.get("remember", False)

    user = User.getByUsername(username)

    if user is None:
        return render_template('index.html', error=ERR_BAD_LOGIN)
    elif user.verify_password(password):
        resp = make_response(redirect(url_for('todo')))
        if remember:
            resp.set_cookie("username", username, max_age=COOKIE_TIMEOUT)
            resp.set_cookie("login_token", user.new_cookie(), max_age=COOKIE_TIMEOUT)
        return resp
    else:
        return render_template('index.html', error=ERR_BAD_LOGIN)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if len(username) < 2:
        return render_template("register.html", error=ERR_BAD_USERNAME)
    if len(password) < 8:
        return render_template("register.html", error=ERR_BAD_PASSWORD)
    user = User.createUser(username, password)
    if not user:
        return render_template("register.html", error=ERR_USERNAME_TAKEN)
    return redirect(url_for('todo'))


@app.route('/todo', methods=['GET'])
def todo():
    if request.method == "GET":
        return render_template("todo.html")
    return "Nada yet"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
