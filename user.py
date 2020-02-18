#!/usr/bin/env python3

import json
from hashlib import sha256
from os import urandom
from base64 import b64encode
from datetime import datetime
from datetime import timedelta


class User():
    _users = {}

    def __init__(self, username):
        self.username = username
        self.todos = []

    def json(self):
        return json.dumps(self.json_dict())

    def json_dict(self):
        return {
            "username": self.username,
            "todos": [t.json_dict() for t in self.todos]
            }

    def verify_cookie(self, cookie):
        now = datetime.now()
        self.cookies = {a: b for a, b in self.cookies.items() if b > now}
        return self.cookies.get(cookie) is not None

    def verify_password(self, password):
        return self._hmac(password) == self.hash

    def verify_session(self, session):
        now = datetime.now()
        self.sessions = {a: b for a, b in self.sessions.items() if b > now}
        return self.sessions.get(session) is not None

    def new_cookie(self):
        cookie = b64encode(urandom(128)).decode('utf-8')
        self.cookies[cookie] = datetime.now() + timedelta(days=30)
        return cookie

    def new_session(self):
        session = b64encode(urandom(128)).decode('utf-8')
        self.sessions[session] = datetime.now() + timedelta(minutes=5)
        return session

    def extend_session(self, session):
        self.sessions[session] = datetime.now() + timedelta(minutes=5)

    def _hmac(self, password):
        inner = sha256(self.salt + password.encode("utf-8")).digest()
        return sha256(self.salt + inner).hexdigest()

    def needs_reset(self, cookie):
        if not self.verify_cookie(cookie):
            return False
        expires = self.cookies[cookie]
        return datetime.now() + timedelta(days=15) > expires

    def invalidate_cookie(self, cookie):
        if cookie in self.cookies:
            del self.cookies[cookie]

    @staticmethod
    def getByUsername(username):
        return User._users.get(username)

    @classmethod
    def createUser(cls, username, password):
        if username in cls._users:
            return None
        inst = cls(username)
        inst.cookies = {}
        inst.sessions = {}
        inst.username = username
        inst.salt = urandom(128)
        inst.hash = inst._hmac(password)
        cls._users[username] = inst
        return inst
