#!/usr/bin/env python3

from hashlib import sha256
from os import urandom
from base64 import b64encode
from datetime import datetime
from datetime import timedelta


class User():
    _users = {}
    _api_tokens = {}

    def __init__(self, username):
        self.username = username

    def verify_cookie(self, cookie):
        now = datetime.now()
        self.cookies = {a: b for a, b in self.cookies.items() if b > now}
        return self.cookies.get(cookie) is not None

    def verify_password(self, password):
        return self._hash(password) == self.hash

    def new_cookie(self):
        cookie = b64encode(urandom(128)).decode('utf-8')
        self.cookies[cookie] = datetime.now() + timedelta(days=30)
        return cookie

    def _hash(self, password):
        return sha256((self.salt + password).encode("utf-8")).hexdigest()

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
        inst.username = username
        inst.salt = b64encode(urandom(128)).decode('utf-8')
        inst.hash = inst._hash(password)
        cls._users[username] = inst
        return inst
