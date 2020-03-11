#!/usr/bin/env python3

from notify import Notification
import json
import secrets


class Todo:
    def __init__(self, title):
        self.id = secrets.token_hex(16)
        self.title = title
        self.active = True
        self.todos = []
        self._notify = []

    def __repr__(self):
        return f"Todo(title={self.title!r})"

    def create_notification(self, start, repeat=None):
        self._notify.append(
            Notification(self.title, "", start, repeat, -1))

    @staticmethod
    def find_by_id(iterable, _id):
        for todo in iterable:
            if todo.id == _id:
                return todo
            a = Todo.find_by_id(todo.todos, _id)
            if a:
                return a
        return None

    @staticmethod
    def delete_by_id(iterable, _id):
        for i in range(len(iterable)):
            if iterable[i].id == _id:
                del iterable[i]
                return True
            if Todo.delete_by_id(iterable[i].todos, _id):
                return True
        return False

    def json(self):
        return json.dumps(self.json_dict)

    def json_dict(self):
        return {
            "title": self.title,
            "id": self.id,
            "active": self.active,
            "todos": [a.json_dict() for a in self.todos]
            }

    def cancel(self):
        self.active = False
        for thread in self._notification_threads:
            thread.cancel()
