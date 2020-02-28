#!/usr/bin/env python3

from notify import Notification
import json


class Todo:
    def __init__(self, title, desc=""):
        self.title = title
        self.desc = desc
        self.active = True
        self.todos = []
        self._notify = []

    def __repr__(self):
        return f"Todo(title={self.title!r}, desc={self.desc!r})"

    def create_notification(self, start, repeat=None):
        self._notify.append(
            Notification(self.title, self.desc, start, repeat, -1))

    def json(self):
        return json.dumps(self.json_dict)

    def json_dict(self):
        return {
            "title": self.title,
            "desc": self.desc,
            "active": self.active,
            "todos": [a.json_dict() for a in self.todos]
            }

    def cancel(self):
        self.active = False
        for thread in self._notification_threads:
            thread.cancel()
