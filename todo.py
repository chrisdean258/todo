#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import json


class Project:
    def __init__(self, title, desc=""):
        self.title = title
        self.desc = desc
        self.subprojects = []
        self.todos = []

    def json(self):
        return json.dumps(self.json_dict())

    def json_dict(self):
        return {
            "title": self.title,
            "desc": self.desc,
            "subprojects": [a.json_dict() for a in self.subprojects],
            "todos": [a.json_dict() for a in self.todos]
            }


class Todo:
    def __init__(self, title, desc="", start=None, end=None, notify=None):
        self.title = title
        self.desc = desc
        self.start = start or datetime.now()
        self.end = end
        self._notify = notify
        if self.end and self.notify is None:
            self.notify = [self.end + timedelta(minutes=-30)]
        self.active = True
        self._notification_threads = []

    def json(self):
        return json.dumps(self.json_dict)

    def json_dict(self):
        return {
            "title": self.title,
            "desc": self.desc,
            "active": self.active
            }

    def cancel(self):
        self.active = False
        for thread in self._notification_threads:
            thread.cancel()


def main():
    p = Project("Test Project")
    p.subprojects.append(Todo("Test todo"))
    p.todos.append(Todo("Test todo 2"))
    print(p.json())


if __name__ == "__main__":
    main()
