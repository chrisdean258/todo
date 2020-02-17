#!/usr/bin/env python3

# import pushbullet
import threading
import time
import queue
import pushbullet
import os
from datetime import datetime, timedelta


api_key = os.environ["PUSHBULLET_API_TOKEN"]
pb = pushbullet.Pushbullet(api_key)


class Notification(threading.Thread):
    scheduler = None
    lock = threading.Lock()
    queue = queue.Queue()

    @staticmethod
    def setup():
        threads = []
        while True:
            threads.append(Notification.queue.get())
            with threads[-1].lock:
                threads[-1].start()
            join = [t for t in threads if not t.is_alive()]
            for thread in join:
                thread.join()
            threads = [t for t in threads if t.is_alive()]

    def __init__(self, title, body, starttime, repeat=None, times=1):
        with Notification.lock:
            if Notification.scheduler is None:
                t = threading.Thread(target=Notification.setup, daemon=True)
                Notification.scheduler = t
                t.start()

        super().__init__()
        self.title = title
        self.body = body
        self.starttime = starttime
        self.repeat = repeat
        self.times = times
        self.alive = True
        self.lock = threading.Lock()
        with self.lock:
            Notification.queue.put(self)

    def send_sleep(self):
        self.send_notification()
        time.sleep(self.repeat.seconds)

    def run(self):
        wait = (self.starttime - datetime.now()).seconds
        time.sleep(wait)
        for i in range(self.times):
            if not self.alive:
                return
            self.send_sleep()
        while self.times < 0 and self.alive:
            self.send_sleep()

    def send_notification(self):
        global pushbullet
        pb.push_note(self.title, self.body)

    def cancel(self):
        with self.lock:
            self.alive = False


def main():
    a = timedelta(seconds=5)
    Notification("Test Title", "Test body", datetime.now() + a, a, times=3)
    time.sleep(1)
    # b.cancel()


if __name__ == "__main__":
    main()
