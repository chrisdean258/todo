#!/usr/bin/env python3

from hashlib import sha256
from os import urandom


class User():
    _users = {}

    def __init__(self, username):
        self.username = username

    def verify_cookie(self, cookie):
        return self.cookie == cookie

    def verify_password(self, password):
        test_hash = sha256((self.salt + password).encode("utf-8")).hexdigest()
        return test_hash == self.hash

    def new_cookie(self):
        self.cookie = str(urandom(128))
        return self.cookie

    @staticmethod
    def getByUsername(username):
        return User._users.get(username)

    @classmethod
    def createUser(cls, username, password):
        if username in cls._users:
            return None
        inst = cls(username)
        inst.salt = str(urandom(128))
        inst.cookie = str(urandom(128))
        inst.hash = sha256((inst.salt + password).encode("utf-8")).hexdigest()
        cls._users[username] = inst
        return inst
