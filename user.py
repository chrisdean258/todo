#!/usr/bin/env python3

import json
import pickle
import redis
from base64 import b64encode
from datetime import datetime
from collections import deque
from datetime import timedelta
from functools import wraps
from hashlib import sha256
from os import urandom
from todo import Todo


def save(func):
    @wraps(func)
    def f(user, *args, **kwargs):
        rtn = func(user, *args, **kwargs)
        User._users[user.username] = user
        return rtn
    return f


class CachedRedisDict:
    def __init__(self, prefix="", size=10, *args, **kwargs):
        self.redis = redis.Redis(*args, **kwargs)
        self.size = size
        self.items = deque()
        self.prefix = prefix

    def __getitem__(self, key):
        key = key + self.prefix
        # for ikey, value in self.items:
        # if key == ikey:
        # return value
        # self._cache(key, rv)
        rv = self.redis.get(key)
        if rv:
            rv = pickle.loads(rv)
        return rv

    def _cache(self, key, value):
        key = key + self.prefix
        vals = [v for k, v in self.items if k == key]
        if len(vals) > 1:
            raise Exception(f"Bad cache: {key} appeared {len(vals)} times")
        if len(vals) == 1:
            self.items = deque([v for k, v in self.items if k != key])
        self.items.append((key, value))
        while len(self.items) > self.size:
            key, value = self.items.popleft()
            self.redis.set(key, pickle.dumps(value))

    def __contains__(self, key):
        # key = key + self.prefix
        return self[key] is not None

    def __setitem__(self, key, value):
        key = key + self.prefix
        self.redis.set(key, pickle.dumps(value))
        # self._cache(key, value)


class User():
    _users = CachedRedisDict(prefix="user:", size=0)
    _api_tokens = CachedRedisDict(prefix="api_key:", size=0)

    def __init__(self, username):
        self.username = username
        self.todos = []

    def __repr__(self):
        return f"User(username={self.username!r})"

    def toJSON(self):
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

    @save
    def new_cookie(self):
        cookie = b64encode(urandom(128)).decode('utf-8')
        self.cookies[cookie] = datetime.now() + timedelta(days=30)
        return cookie

    @save
    def new_session(self):
        session = b64encode(urandom(128)).decode('utf-8')
        self.sessions[session] = datetime.now() + timedelta(minutes=5)
        return session

    @save
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

    @save
    def delete_todo_by_id(self, todoid):
        Todo.delete_by_id(self.todos, todoid)

    @save
    def invalidate_cookie(self, cookie):
        if cookie in self.cookies:
            del self.cookies[cookie]

    @save
    def new_todo(self, parent_id, *args, **kwargs):
        if parent_id == "" or parent_id == "todos":
            self.todos.append(Todo(*args, **kwargs))
        else:
            parent = Todo.find_by_id(self.todos, parent_id)
            if parent:
                parent.todos.append(Todo(*args, **kwargs))

    @staticmethod
    def getByUsername(username):
        retval = User._users[username]
        if not retval:
            return None
        if not isinstance(retval, User):
            return None
        return retval

    @classmethod
    def createUser(cls, username, password):
        if cls.getByUsername(username):
            return None
        inst = cls(username)
        inst.cookies = {}
        inst.sessions = {}
        inst.username = username
        inst.salt = urandom(128)
        inst.hash = inst._hmac(password)
        cls._users[username] = inst
        return inst
