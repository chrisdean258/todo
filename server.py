#!/usr/bin/env python3

from flask import Flask
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from user import User

app = Flask(__name__)


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
        return render_template('index.html', error="Bad username or password")
    elif user.verify_password(password):
        resp = make_response(redirect(url_for('todo')))
        if remember:
            resp.set_cookie("login_token", user.new_cookie())
        return resp
    else:
        return render_template('index.html', error="Bad username or password")

@app.route('/register')
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    


@app.route('/todo', methods=['GET'])
def todo():
    if request.method == "GET":
        return render_template("todo.html")
    return "Nada yet"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
