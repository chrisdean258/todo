#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta


class Todo:
    def __init__(self, title, desc="", start=None, end=None, notify=None):
        self.title = title
        self.desc = desc
        self.start = start or datetime.now()
        self.end = end
        self.notify = notify
        if self.end and self.notify is None:
            self.notify = [self.end + timedelta(minutes=-30)]
