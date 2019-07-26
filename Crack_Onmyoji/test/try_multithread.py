import threading


class MyThread(threading.Thread):
    def __init__(self, thread_id):
        super(MyThread, self).__init__()
        self.thread_id = thread_id
        self.message = 0

    def run(self):
        return
